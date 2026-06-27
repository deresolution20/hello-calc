"""Acceptance tests for configuring ruff and mypy --strict tooling.

These tests validate that:
1. `ruff check src/` executes successfully on the empty package.
2. `mypy --strict src/` executes successfully on the empty package.
3. Tooling configuration files or pyproject.toml sections are committed to the repo.
"""

import os
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_ruff_check_src_exits_successfully():
    """ruff check src/ should be runnable and exit 0 on the empty package."""
    result = subprocess.run(
        ["ruff", "check", "src/"],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"ruff check src/ failed with exit code {result.returncode}.\n"
        f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )


def test_mypy_strict_src_exits_successfully():
    """mypy --strict src/ should be runnable and exit 0 on the empty package."""
    result = subprocess.run(
        ["mypy", "--strict", "src/"],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"mypy --strict src/ failed with exit code {result.returncode}.\n"
        f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )


def test_ruff_configuration_is_committed():
    """A ruff configuration file or pyproject.toml section should exist in the repo."""
    ruff_config_files = [
        REPO_ROOT / "ruff.toml",
        REPO_ROOT / ".ruff.toml",
    ]

    found_ruff_file = any(f.exists() for f in ruff_config_files)

    pyproject = REPO_ROOT / "pyproject.toml"
    found_ruff_in_pyproject = False
    if pyproject.exists():
        content = pyproject.read_text()
        found_ruff_in_pyproject = "[tool.ruff" in content

    assert found_ruff_file or found_ruff_in_pyproject, (
        "No ruff configuration found. Expected ruff.toml, .ruff.toml, "
        "or a [tool.ruff] section in pyproject.toml."
    )


def test_mypy_configuration_is_committed():
    """A mypy configuration file or pyproject.toml section should exist in the repo."""
    mypy_config_files = [
        REPO_ROOT / "mypy.ini",
        REPO_ROOT / ".mypy.ini",
        REPO_ROOT / "setup.cfg",
    ]

    found_mypy_file = False
    for cfg_file in mypy_config_files:
        if cfg_file.exists():
            content = cfg_file.read_text()
            if cfg_file.name == "setup.cfg":
                found_mypy_file = "[mypy" in content
            else:
                found_mypy_file = True
                break

    pyproject = REPO_ROOT / "pyproject.toml"
    found_mypy_in_pyproject = False
    if pyproject.exists():
        content = pyproject.read_text()
        found_mypy_in_pyproject = "[tool.mypy" in content

    assert found_mypy_file or found_mypy_in_pyproject, (
        "No mypy configuration found. Expected mypy.ini, .mypy.ini, "
        "a [mypy] section in setup.cfg, or a [tool.mypy] section in pyproject.toml."
    )


def test_src_directory_exists():
    """The src/ directory should exist since both tools target it."""
    src_dir = REPO_ROOT / "src"
    assert src_dir.exists() and src_dir.is_dir(), (
        f"src/ directory not found at {src_dir}"
    )