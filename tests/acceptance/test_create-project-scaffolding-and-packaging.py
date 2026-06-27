"""Acceptance tests for project scaffolding and packaging metadata of hello-calc."""
import sys
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
PYPROJECT_TOML = REPO_ROOT / "pyproject.toml"
INIT_FILE = REPO_ROOT / "src" / "hello_calc" / "__init__.py"


def test_pyproject_toml_exists():
    """AC 1: pyproject.toml exists."""
    assert PYPROJECT_TOML.is_file(), f"pyproject.toml not found at {PYPROJECT_TOML}"


def test_pyproject_toml_contains_project_name_and_src_layout():
    """AC 1: pyproject.toml contains project name 'hello-calc' and src layout configuration."""
    if not PYPROJECT_TOML.is_file():
        pytest.fail("pyproject.toml does not exist")
    
    content = PYPROJECT_TOML.read_text()
    assert "hello-calc" in content, "Project name 'hello-calc' not found in pyproject.toml"
    assert "src" in content, "src layout configuration not found in pyproject.toml"


def test_init_file_exists():
    """AC 2: src/hello_calc/__init__.py exists."""
    assert INIT_FILE.is_file(), f"__init__.py not found at {INIT_FILE}"


def test_pip_install_editable_completes_without_error():
    """AC 3: `pip install -e .` completes without error."""
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "-e", "."],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, (
        f"pip install -e . failed with return code {result.returncode}\n"
        f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
    )


def test_import_hello_calc_succeeds_after_install():
    """AC 4: `python -c 'import hello_calc'` succeeds after install."""
    result = subprocess.run(
        [sys.executable, "-c", "import hello_calc"],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, (
        f"python -c 'import hello_calc' failed with return code {result.returncode}\n"
        f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
    )