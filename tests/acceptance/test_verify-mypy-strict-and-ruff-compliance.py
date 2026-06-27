"""Acceptance tests for verifying mypy --strict and ruff compliance.

These tests validate that:
1. `mypy --strict src/` produces no errors
2. `ruff check src/` produces no errors
3. All existing unit tests still pass after any fixes
4. `pip install -e .` still succeeds
"""

import subprocess
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = PROJECT_ROOT / "src"


def test_mypy_strict_produces_no_errors():
    """mypy --strict src/ should produce no errors."""
    result = subprocess.run(
        [sys.executable, "-m", "mypy", "--strict", "src/"],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"mypy --strict src/ failed with exit code {result.returncode}:\n"
        f"STDOUT:\n{result.stdout}\n"
        f"STDERR:\n{result.stderr}"
    )


def test_ruff_check_produces_no_errors():
    """ruff check src/ should produce no errors."""
    result = subprocess.run(
        [sys.executable, "-m", "ruff", "check", "src/"],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"ruff check src/ failed with exit code {result.returncode}:\n"
        f"STDOUT:\n{result.stdout}\n"
        f"STDERR:\n{result.stderr}"
    )


def test_existing_unit_tests_still_pass():
    """All existing unit tests should still pass after any fixes."""
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "tests/",
            "-x",
            "--ignore=tests/acceptance",
        ],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"Unit tests failed with exit code {result.returncode}:\n"
        f"STDOUT:\n{result.stdout}\n"
        f"STDERR:\n{result.stderr}"
    )


def test_pip_install_editable_succeeds():
    """pip install -e . should still succeed."""
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "-e", "."],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"pip install -e . failed with exit code {result.returncode}:\n"
        f"STDOUT:\n{result.stdout}\n"
        f"STDERR:\n{result.stderr}"
    )