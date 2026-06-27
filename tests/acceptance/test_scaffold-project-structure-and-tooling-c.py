"""
Acceptance tests for the scaffold project structure and tooling configuration task.

These tests validate that:
1. pyproject.toml exists with the correct package name and build configuration
2. src/hello_calc/__init__.py exists
3. The package is installable with `pip install -e .`
4. Ruff is configured in pyproject.toml
5. Mypy is configured with strict mode in pyproject.toml
"""

import subprocess
import sys
from pathlib import Path

import pytest
import tomllib


PROJECT_ROOT = Path(__file__).resolve().parents[2]
PYPROJECT_PATH = PROJECT_ROOT / "pyproject.toml"
INIT_PATH = PROJECT_ROOT / "src" / "hello_calc" / "__init__.py"


@pytest.fixture(scope="module")
def pyproject_data():
    """Load and parse pyproject.toml."""
    with open(PYPROJECT_PATH, "rb") as f:
        return tomllib.load(f)


def test_pyproject_toml_exists():
    """Acceptance Criterion 1a: pyproject.toml file exists."""
    assert PYPROJECT_PATH.is_file(), f"pyproject.toml not found at {PYPROJECT_PATH}"


def test_pyproject_toml_has_package_name_hello_calc(pyproject_data):
    """Acceptance Criterion 1b: pyproject.toml contains package name hello-calc."""
    name = pyproject_data.get("project", {}).get("name")
    assert name == "hello-calc", f"Expected package name 'hello-calc', got '{name}'"


def test_pyproject_toml_has_version(pyproject_data):
    """Acceptance Criterion 1c: pyproject.toml contains a version."""
    version = pyproject_data.get("project", {}).get("version")
    assert version is not None, "Package version not found in pyproject.toml"


def test_pyproject_toml_requires_python_gte_3_9(pyproject_data):
    """Acceptance Criterion 1d: pyproject.toml requires Python >=3.9."""
    requires_python = pyproject_data.get("project", {}).get("requires-python", "")
    assert "3.9" in requires_python, f"Expected requires-python to include 3.9, got '{requires_python}'"


def test_pyproject_toml_has_build_system(pyproject_data):
    """Acceptance Criterion 1e: pyproject.toml has a build system configured."""
    build_system = pyproject_data.get("build-system", {})
    requires = build_system.get("requires", [])
    assert len(requires) > 0, "No build-system requires found in pyproject.toml"
    build_backend = build_system.get("build-backend")
    assert build_backend is not None, "No build-backend found in pyproject.toml"


def test_src_hello_calc_init_exists():
    """Acceptance Criterion 2: src/hello_calc/__init__.py exists."""
    assert INIT_PATH.is_file(), f"__init__.py not found at {INIT_PATH}"


def test_src_hello_calc_init_is_empty_or_valid_python():
    """Acceptance Criterion 2: src/hello_calc/__init__.py is valid Python (can be empty)."""
    content = INIT_PATH.read_text()
    # Compile to verify it's valid Python (empty file is valid)
    compile(content, str(INIT_PATH), "exec")


def test_pip_install_editable_succeeds():
    """Acceptance Criterion 3: `pip install -e .` succeeds without errors."""
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "-e", ".", "--no-build-isolation"],
        capture_output=True,
        text=True,
        cwd=str(PROJECT_ROOT),
    )
    assert result.returncode == 0, (
        f"`pip install -e .` failed with return code {result.returncode}.\n"
        f"stdout:\n{result.stdout}\n\nstderr:\n{result.stderr}"
    )


def test_ruff_configured_in_pyproject(pyproject_data):
    """Acceptance Criterion 4: ruff is configured in pyproject.toml."""
    # Ruff can be configured under [tool.ruff] section
    tool = pyproject_data.get("tool", {})
    ruff_config = tool.get("ruff")
    assert ruff_config is not None, "No [tool.ruff] section found in pyproject.toml"


def test_mypy_configured_with_strict_mode(pyproject_data):
    """Acceptance Criterion 5: mypy is configured with strict mode in pyproject.toml."""
    tool = pyproject_data.get("tool", {})
    mypy_config = tool.get("mypy")
    assert mypy_config is not None, "No [tool.mypy] section found in pyproject.toml"
    strict = mypy_config.get("strict", False)
    assert strict is True, "mypy strict mode is not enabled in pyproject.toml"