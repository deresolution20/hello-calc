"""
Acceptance tests for the core arithmetic functions task.

These tests validate that:
- add, subtract, multiply, and divide return the expected float results.
- divide raises ValueError on zero divisor with the proper message.
- The source file passes mypy --strict and ruff check without errors.
"""

import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from hello_calc.calc import add, divide, multiply, subtract

SRC_PATH = Path(__file__).resolve().parents[2] / "src" / "hello_calc" / "calc.py"


def test_add_returns_float_5():
    assert add(2, 3) == 5.0


def test_subtract_returns_float_6():
    assert subtract(10, 4) == 6.0


def test_multiply_returns_float_12():
    assert multiply(3, 4) == 12.0


def test_divide_returns_float_5():
    assert divide(10, 2) == 5.0


def test_divide_by_zero_raises_value_error():
    with pytest.raises(ValueError) as exc_info:
        divide(1, 0)
    assert "division by zero" in str(exc_info.value)


def test_functions_return_float_type():
    assert isinstance(add(2, 3), float)
    assert isinstance(subtract(10, 4), float)
    assert isinstance(multiply(3, 4), float)
    assert isinstance(divide(10, 2), float)


@pytest.mark.skipif(shutil.which("mypy") is None, reason="mypy not installed")
def test_mypy_strict_passes():
    result = subprocess.run(
        [sys.executable, "-m", "mypy", "--strict", str(SRC_PATH)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"mypy --strict failed:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
    )


@pytest.mark.skipif(shutil.which("ruff") is None, reason="ruff not installed")
def test_ruff_check_passes():
    src_dir = str(SRC_PATH.parent.parent)
    result = subprocess.run(
        [sys.executable, "-m", "ruff", "check", src_dir],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"ruff check failed:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
    )