"""Acceptance tests for the project scaffolding task.

These tests validate that the minimal Python package structure is in place
so that `pip install -e .` works, the package is importable after install,
and the required packaging metadata file exists with the correct package name.
"""

import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture(scope="module")
def pip_install_result():
    """Run `pip install -e .` once for this test module and return the result."""
    return subprocess.run(
        [sys.executable, "-m", "pip", "install", "-e", "."],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
    )


def test_pip_install_editable_succeeds(pip_install_result):
    """AC1: Running `pip install -e .` from the repository root succeeds."""
    assert pip_install_result.returncode == 0, (
        f"pip install -e . failed with return code {pip_install_result.returncode}\n"
        f"stdout:\n{pip_install_result.stdout}\n"
        f"stderr:\n{pip_install_result.stderr}"
    )


def test_import_hello_calc_after_install(pip_install_result):
    """AC2: After install, `python -c "import hello_calc"` runs without error."""
    # Ensure the install succeeded before checking import
    assert pip_install_result.returncode == 0, (
        "Cannot test import because pip install -e . failed:\n"
        f"{pip_install_result.stderr}"
    )
    result = subprocess.run(
        [sys.executable, "-c", "import hello_calc"],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"import hello_calc failed with return code {result.returncode}\n"
        f"stdout:\n{result.stdout}\n"
        f"stderr:\n{result.stderr}"
    )


def test_packaging_file_exists_with_package_metadata():
    """AC3: A pyproject.toml (or equivalent) exists with package metadata for `hello-calc`."""
    candidate_files = [
        REPO_ROOT / "pyproject.toml",
        REPO_ROOT / "setup.py",
        REPO_ROOT / "setup.cfg",
    ]
    existing_files = [f for f in candidate_files if f.exists()]
    assert len(existing_files) > 0, (
        "No packaging file found: expected pyproject.toml, setup.py, or setup.cfg "
        f"in {REPO_ROOT}"
    )

    combined_content = ""
    for f in existing_files:
        combined_content += f.read_text()

    assert "hello-calc" in combined_content or "hello_calc" in combined_content, (
        "Package name 'hello-calc' (or 'hello_calc') not found in any packaging file"
    )