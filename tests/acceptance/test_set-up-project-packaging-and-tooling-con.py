"""Acceptance tests for setting up project packaging and tooling configuration.

These tests validate that:
1. pyproject.toml exists with package name hello_calc and src/ layout configured
2. pip install -e . completes without errors from a clean clone
3. python -c "import hello_calc" succeeds after install
4. ruff and mypy are declared as dev dependencies or optional dependencies
"""

import os
import subprocess
import sys

import pytest

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)
)
PYPROJECT_PATH = os.path.join(PROJECT_ROOT, "pyproject.toml")


@pytest.fixture(scope="module")
def pyproject_data():
    """Load and parse pyproject.toml."""
    with open(PYPROJECT_PATH, "rb") as f:
        return tomllib.load(f)


class TestPyprojectExists:
    """Acceptance Criterion 1: pyproject.toml exists with package name
    hello_calc and src/ layout configured."""

    def test_pyproject_toml_exists(self):
        assert os.path.isfile(PYPROJECT_PATH), "pyproject.toml must exist at project root"

    def test_package_name_is_hello_calc(self, pyproject_data):
        name = pyproject_data.get("project", {}).get("name")
        assert name == "hello_calc", f"Expected package name 'hello_calc', got '{name}'"

    def test_src_layout_configured(self, pyproject_data):
        """The src/ layout should be configured via setuptools package discovery
        or hatchling/other build backends."""
        # Check for setuptools src layout configuration
        setuptools_cfg = pyproject_data.get("tool", {}).get("setuptools", {})
        packages_find = setuptools_cfg.get("packages", {})

        # Option A: [tool.setuptools.packages.find] with where = ["src"]
        if "find" in setuptools_cfg.get("packages", {}):
            where = packages_find.get("where", [])
            assert "src" in where, "src/ layout not configured in packages.find.where"
            return

        # Option B: [tool.setuptools] package-dir mapping
        package_dir = setuptools_cfg.get("package-dir", {})
        if package_dir:
            assert package_dir.get("") == "src" or any(
                v == "src" for v in package_dir.values()
            ), "src/ layout not configured in package-dir"
            return

        # Option C: hatch build config with src in packages
        hatch_cfg = pyproject_data.get("tool", {}).get("hatch", {}).get("build", {})
        if hatch_cfg:
            packages = hatch_cfg.get("packages", [])
            assert "src/hello_calc" in packages or "src" in packages, (
                "src/ layout not configured for hatch"
            )
            return

        pytest.fail("No src/ layout configuration found in pyproject.toml")

    def test_build_system_declared(self, pyproject_data):
        build_system = pyproject_data.get("build-system", {})
        assert "requires" in build_system, "build-system.requires must be declared"
        assert "build-backend" in build_system, "build-system.build-backend must be declared"

    def test_src_hello_calc_directory_exists(self):
        src_path = os.path.join(PROJECT_ROOT, "src", "hello_calc")
        assert os.path.isdir(src_path), "src/hello_calc/ directory must exist"


class TestEditableInstall:
    """Acceptance Criterion 2: pip install -e . completes without errors."""

    @pytest.fixture(scope="class", autouse=True)
    def editable_install(self):
        """Perform an editable install and clean up afterward."""
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-e", "."],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
        )
        yield result
        # Uninstall after tests
        subprocess.run(
            [sys.executable, "-m", "pip", "uninstall", "-y", "hello_calc"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
        )

    def test_pip_install_editable_succeeds(self, editable_install):
        result = editable_install
        assert result.returncode == 0, (
            f"pip install -e . failed with return code {result.returncode}\n"
            f"stdout: {result.stdout}\n"
            f"stderr: {result.stderr}"
        )


class TestImportAfterInstall:
    """Acceptance Criterion 3: python -c "import hello_calc" succeeds after install."""

    @pytest.fixture(scope="class", autouse=True)
    def editable_install(self):
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-e", "."],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
        )
        yield result
        subprocess.run(
            [sys.executable, "-m", "pip", "uninstall", "-y", "hello_calc"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
        )

    def test_import_hello_calc_succeeds(self):
        result = subprocess.run(
            [sys.executable, "-c", "import hello_calc"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, (
            f"import hello_calc failed with return code {result.returncode}\n"
            f"stdout: {result.stdout}\n"
            f"stderr: {result.stderr}"
        )


class TestDevDependencies:
    """Acceptance Criterion 4: ruff and mypy are declared as dev dependencies
    or optional dependencies."""

    def test_ruff_and_mypy_declared(self, pyproject_data):
        all_deps = set()

        # Check optional dependencies (e.g., [project.optional-dependencies])
        optional_deps = pyproject_data.get("project", {}).get("optional-dependencies", {})
        for group_deps in optional_deps.values():
            for dep in group_deps:
                all_deps.add(dep.lower())

        # Check dependency-groups (PEP 735)
        dep_groups = pyproject_data.get("dependency-groups", {})
        for group_deps in dep_groups.values():
            for dep in group_deps:
                all_deps.add(dep.lower())

        # Check [tool.uv] dev-dependencies
        uv_dev = pyproject_data.get("tool", {}).get("uv", {}).get("dev-dependencies", [])
        for dep in uv_dev:
            all_deps.add(dep.lower())

        # Check [tool.poetry.group.dev.dependencies]
        poetry_groups = pyproject_data.get("tool", {}).get("poetry", {}).get("group", {})
        for group_name, group_cfg in poetry_groups.items():
            for dep in group_cfg.get("dependencies", {}):
                all_deps.add(dep.lower())

        # Check main dependencies as fallback
        main_deps = pyproject_data.get("project", {}).get("dependencies", [])
        for dep in main_deps:
            all_deps.add(dep.lower())

        # Verify ruff
        ruff_found = any("ruff" in dep for dep in all_deps)
        assert ruff_found, "ruff is not declared as a dev or optional dependency"

        # Verify mypy
        mypy_found = any("mypy" in dep for dep in all_deps)
        assert mypy_found, "mypy is not declared as a dev or optional dependency"


class TestToolingConfiguration:
    """Validate that ruff and mypy have configuration sections set to strict rules."""

    def test_ruff_config_exists(self, pyproject_data):
        ruff_cfg = pyproject_data.get("tool", {}).get("ruff")
        assert ruff_cfg is not None, "[tool.ruff] configuration section must exist"

    def test_ruff_strict_rules(self, pyproject_data):
        ruff_cfg = pyproject_data.get("tool", {}).get("ruff", {})
        # Check for lints section with strict rules
        lint_cfg = ruff_cfg.get("lint", {})
        select = lint_cfg.get("select", [])
        # Strict typically includes E, F, I, or "ALL"
        assert len(select) > 0, (
            "ruff lint.select must specify rules (e.g., ['E', 'F', 'I'] or ['ALL'])"
        )

    def test_mypy_config_exists(self, pyproject_data):
        mypy_cfg = pyproject_data.get("tool", {}).get("mypy")
        assert mypy_cfg is not None, "[tool.mypy] configuration section must exist"

    def test_mypy_strict_rules(self, pyproject_data):
        mypy_cfg = pyproject_data.get("tool", {}).get("mypy", {})
        strict = mypy_cfg.get("strict")
        assert strict is not None and (
            strict is True or strict == "" or strict == "True"
        ), "mypy strict mode must be enabled (strict = true)"