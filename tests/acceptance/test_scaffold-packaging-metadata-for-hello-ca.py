"""Acceptance tests for scaffolding packaging metadata for hello-calc.

These tests validate that the minimal project configuration needed to install
the hello_calc package in editable mode has been correctly created.
They cover:
  - pip install -e . succeeding from the project root
  - pyproject.toml declaring hello-calc with a valid version string
  - Package discovery configured to find hello_calc under src/
  - mypy and ruff listed as dev or optional dependencies
"""

import re
import subprocess
import sys
from pathlib import Path

import pytest

try:
    import tomllib
except ImportError:
    tomllib = pytest.importorskip("tomli")

# Resolve project root relative to this test file:
# tests/acceptance/test_scaffold...py -> ../../ -> project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
PYPROJECT_PATH = PROJECT_ROOT / "pyproject.toml"
SRC_PACKAGE_PATH = PROJECT_ROOT / "src" / "hello_calc"


def load_pyproject():
    """Load and return the parsed contents of pyproject.toml."""
    assert PYPROJECT_PATH.is_file(), f"pyproject.toml not found at {PYPROJECT_PATH}"
    with open(PYPROJECT_PATH, "rb") as f:
        return tomllib.load(f)


# ---------------------------------------------------------------------------
# Acceptance Criterion 1: pip install -e . succeeds from the project root
# ---------------------------------------------------------------------------

class TestPipInstallEditable:
    """Validate that `pip install -e .` completes successfully."""

    def test_pip_install_editable_succeeds(self):
        """pip install -e . should exit with return code 0."""
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-e", "."],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, (
            f"pip install -e . failed (exit {result.returncode}).\n"
            f"stdout:\n{result.stdout}\n"
            f"stderr:\n{result.stderr}"
        )

    def test_hello_calc_importable_after_install(self):
        """The installed package should be importable as hello_calc."""
        result = subprocess.run(
            [sys.executable, "-c", "import hello_calc; print(hello_calc.__file__)"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, (
            f"Failed to import hello_calc after editable install.\n"
            f"stderr:\n{result.stderr}"
        )


# ---------------------------------------------------------------------------
# Acceptance Criterion 2: pyproject.toml declares hello-calc with valid version
# ---------------------------------------------------------------------------

class TestProjectMetadata:
    """Validate project name and version declared in pyproject.toml."""

    def test_project_name_is_hello_calc(self):
        """The [project] name must be 'hello-calc'."""
        data = load_pyproject()
        name = data.get("project", {}).get("name")
        assert name == "hello-calc", f"Expected project name 'hello-calc', got {name!r}"

    def test_version_string_exists(self):
        """A version string must be present under [project]."""
        data = load_pyproject()
        version = data.get("project", {}).get("version")
        assert version is not None, "No 'version' field found under [project]"

    def test_version_string_is_valid_pep440(self):
        """The version string should conform to PEP 440 (basic check)."""
        data = load_pyproject()
        version = data["project"]["version"]
        # PEP 440 simplified regex: at least digits.digits pattern
        pattern = r"^\d+(\.\d+)*((a|b|rc)\d*)?(\.post\d*)?(\.dev\d*)?$"
        assert re.match(pattern, version), (
            f"Version '{version}' does not look like a valid PEP 440 version"
        )

    def test_requires_python_at_least_38(self):
        """The project should declare a minimum Python version of 3.8+."""
        data = load_pyproject()
        requires_python = data.get("project", {}).get("requires-python", "")
        assert "3.8" in requires_python, (
            f"Expected '3.8' in requires-python, got {requires_python!r}"
        )


class TestBuildSystem:
    """Validate that build-system metadata is present."""

    def test_build_system_declared(self):
        """[build-system] must be present with requires and build-backend."""
        data = load_pyproject()
        build_system = data.get("build-system")
        assert build_system is not None, "[build-system] section is missing"
        assert "requires" in build_system, "build-system.requires is missing"
        assert "build-backend" in build_system, "build-system.build-backend is missing"

    def test_build_backend_specified(self):
        """A concrete build backend must be declared."""
        data = load_pyproject()
        backend = data["build-system"]["build-backend"]
        assert backend, "build-backend must not be empty"


# ---------------------------------------------------------------------------
# Acceptance Criterion 3: Package discovery configured for src/hello_calc
# ---------------------------------------------------------------------------

class TestPackageDiscovery:
    """Validate package discovery configuration and directory layout."""

    def test_src_hello_calc_directory_exists(self):
        """The directory src/hello_calc/ must exist."""
        assert SRC_PACKAGE_PATH.is_dir(), (
            f"Expected directory {SRC_PACKAGE_PATH} but it does not exist"
        )

    def test_hello_calc_has_init_py(self):
        """hello_calc must be a proper Python package with __init__.py."""
        init_file = SRC_PACKAGE_PATH / "__init__.py"
        assert init_file.is_file(), (
            f"Expected {init_file} but it does not exist"
        )

    def test_package_discovery_where_src(self):
        """Setuptools package discovery must point to src/."""
        data = load_pyproject()
        tool_setuptools = data.get("tool", {}).get("setuptools", {})

        # Check [tool.setuptools.packages.find] -> where = ["src"]
        packages_find = tool_setuptools.get("packages", {}).get("find", {})
        if packages_find:
            where = packages_find.get("where", [])
            if isinstance(where, str):
                where = [where]
            assert any(str(p).replace("\\", "/").rstrip("/") == "src" for p in where), (
                f"Expected 'src' in packages.find.where, got {where}"
            )
            return

        # Alternatively check [tool.setuptools.package-dir] -> "" = "src"
        package_dir = tool_setuptools.get("package-dir", {})
        if package_dir:
            assert any("src" in str(v) for v in package_dir.values()), (
                f"Expected 'src' in package-dir values, got {package_dir}"
            )
            return

        pytest.fail(
            "No package discovery configuration found under [tool.setuptools]. "
            "Expected either [tool.setuptools.packages.find] with where=['src'] "
            "or [tool.setuptools.package-dir] with a 'src' value."
        )

    def test_hello_calc_found_by_discovery(self):
        """The discovery configuration should resolve to the hello_calc package."""
        data = load_pyproject()
        tool_setuptools = data.get("tool", {}).get("setuptools", {})

        # Check explicit packages list
        packages = tool_setuptools.get("packages", {})
        if isinstance(packages, list) and "hello_calc" in packages:
            return

        # Check find configuration
        packages_find = packages.get("find", {}) if isinstance(packages, dict) else {}
        if packages_find:
            # If find is configured with where=src, hello_calc should be discoverable
            where = packages_find.get("where", [])
            if isinstance(where, str):
                where = [where]
            for w in where:
                p = PROJECT_ROOT / w
                if (p / "hello_calc" / "__init__.py").is_file():
                    return
            # Or no where means default includes src if package-dir is set
            package_dir = tool_setuptools.get("package-dir", {})
            if package_dir:
                for v in package_dir.values():
                    p = PROJECT_ROOT / str(v)
                    if (p / "hello_calc" / "__init__.py").is_file():
                        return

        pytest.fail("hello_calc package not discoverable from the configured paths")


# ---------------------------------------------------------------------------
# Acceptance Criterion 4: mypy and ruff listed as dev/optional dependencies
# ---------------------------------------------------------------------------

class TestDevDependencies:
    """Validate that mypy and ruff are listed as dev or optional dependencies."""

    @staticmethod
    def _collect_dev_dependencies(data):
        """Gather all dependency strings from optional-dependencies and dependency-groups."""
        deps = []

        # [project.optional-dependencies]
        optional = data.get("project", {}).get("optional-dependencies", {})
        for group_deps in optional.values():
            if isinstance(group_deps, list):
                deps.extend(group_deps)

        # [dependency-groups] (PEP 735)
        dep_groups = data.get("dependency-groups", {})
        for group_deps in dep_groups.values():
            if isinstance(group_deps, list):
                deps.extend(group_deps)

        return deps

    def test_mypy_listed(self):
        """mypy must appear among dev or optional dependencies."""
        data = load_pyproject()
        deps = self._collect_dev_dependencies(data)
        assert any("mypy" in d.lower() for d in deps), (
            "mypy not found in optional-dependencies or dependency-groups"
        )

    def test_ruff_listed(self):
        """ruff must appear among dev or optional dependencies."""
        data = load_pyproject()
        deps = self._collect_dev_dependencies(data)
        assert any("ruff" in d.lower() for d in deps), (
            "ruff not found in optional-dependencies or dependency-groups"
        )

    def test_mypy_and_ruff_not_in_main_dependencies(self):
        """mypy and ruff should not be in the main [project.dependencies] list."""
        data = load_pyproject()
        main_deps = data.get("project", {}).get("dependencies", [])
        for dep in main_deps:
            assert "mypy" not in dep.lower(), (
                "mypy should be a dev/optional dependency, not a main dependency"
            )
            assert "ruff" not in dep.lower(), (
                "ruff should be a dev/optional dependency, not a main dependency"
            )