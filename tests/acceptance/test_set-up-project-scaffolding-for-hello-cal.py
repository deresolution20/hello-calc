"""
Acceptance tests for the 'Set up project scaffolding for hello-calc' task.

These tests validate:
1. pyproject.toml exists with valid build system configuration
2. src/hello_calc/__init__.py exists
3. src/hello_calc/calc.py exists
4. pip install -e . succeeds without errors
5. python -c 'import hello_calc' succeeds after installation
"""
import subprocess
import sys
from pathlib import Path

import pytest
import tomllib


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_pyproject_toml_exists():
    """Acceptance criterion 1 (part a): pyproject.toml file exists."""
    pyproject_path = PROJECT_ROOT / "pyproject.toml"
    assert pyproject_path.exists(), f"Expected pyproject.toml at {pyproject_path}"


def test_pyproject_toml_has_build_system_config():
    """Acceptance criterion 1 (part b): pyproject.toml contains valid build system configuration."""
    pyproject_path = PROJECT_ROOT / "pyproject.toml"
    with open(pyproject_path, "rb") as f:
        data = tomllib.load(f)
    assert "build-system" in data, "pyproject.toml must contain a [build-system] table"
    build_system = data["build-system"]
    assert "requires" in build_system, "[build-system] must have 'requires'"
    assert isinstance(build_system["requires"], list) and len(build_system["requires"]) > 0
    assert "build-backend" in build_system, "[build-system] must have 'build-backend'"
    backend = build_system["build-backend"]
    assert isinstance(backend, str) and backend, "build-backend must be a non-empty string"


def test_pyproject_toml_has_project_metadata():
    """Acceptance criterion 1 (part c): pyproject.toml contains package metadata."""
    pyproject_path = PROJECT_ROOT / "pyproject.toml"
    with open(pyproject_path, "rb") as f:
        data = tomllib.load(f)
    assert "project" in data, "pyproject.toml must contain a [project] table"
    project = data["project"]
    assert "name" in project, "[project] must have a 'name' field"
    assert isinstance(project["name"], str) and project["name"]


def test_pyproject_toml_includes_ruff_and_mypy_dev_dependencies():
    """Acceptance criterion: ruff and mypy are included as dev dependencies."""
    pyproject_path = PROJECT_ROOT / "pyproject.toml"
    with open(pyproject_path, "rb") as f:
        data = tomllib.load(f)

    dev_deps_text = ""
    # Check optional-dependencies for a dev group
    project = data.get("project", {})
    optional = project.get("optional-dependencies", {})
    for key, deps in optional.items():
        if "dev" in key.lower():
            dev_deps_text += " ".join(deps)

    # Check dependency-groups (PEP 735)
    dep_groups = data.get("dependency-groups", {})
    for key, deps in dep_groups.items():
        if "dev" in key.lower():
            dev_deps_text += " " + " ".join(deps)

    # Check tool.uv dev-dependencies
    uv = data.get("tool", {}).get("uv", {})
    uv_dev = uv.get("dev-dependencies", [])
    dev_deps_text += " " + " ".join(uv_dev)

    assert "ruff" in dev_deps_text.lower(), "ruff must be listed as a dev dependency"
    assert "mypy" in dev_deps_text.lower(), "mypy must be listed as a dev dependency"


def test_src_hello_calc_init_exists():
    """Acceptance criterion 2: src/hello_calc/__init__.py exists."""
    init_path = PROJECT_ROOT / "src" / "hello_calc" / "__init__.py"
    assert init_path.exists(), f"Expected src/hello_calc/__init__.py at {init_path}"
    assert init_path.is_file(), f"{init_path} must be a file"


def test_src_hello_calc_calc_exists():
    """Acceptance criterion 3: src/hello_calc/calc.py exists."""
    calc_path = PROJECT_ROOT / "src" / "hello_calc" / "calc.py"
    assert calc_path.exists(), f"Expected src/hello_calc/calc.py at {calc_path}"
    assert calc_path.is_file(), f"{calc_path} must be a file"


def test_pip_install_editable_succeeds():
    """Acceptance criterion 4: pip install -e . succeeds without errors."""
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "-e", "."],
        cwd=str(PROJECT_ROOT),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"pip install -e . failed with return code {result.returncode}.\n"
        f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )


def test_import_hello_calc_succeeds():
    """Acceptance criterion 5: python -c 'import hello_calc' succeeds after installation."""
    result = subprocess.run(
        [sys.executable, "-c", "import hello_calc"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"import hello_calc failed with return code {result.returncode}.\n"
        f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )