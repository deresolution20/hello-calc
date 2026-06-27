import pytest
import subprocess
import sys

from hello_calc import add, subtract, multiply, divide
import hello_calc


def test_imports_succeed_after_install():
    assert add is not None
    assert subtract is not None
    assert multiply is not None
    assert divide is not None
    assert set(hello_calc.__all__) == {"add", "subtract", "multiply", "divide"}


def test_add_returns_expected_float():
    assert add(2, 3) == 5.0


def test_subtract_returns_expected_float():
    assert subtract(10, 4) == 6.0


def test_multiply_returns_expected_float():
    assert multiply(3, 4) == 12.0


def test_divide_returns_expected_float():
    assert divide(10, 2) == 5.0


def test_divide_by_zero_raises_value_error():
    with pytest.raises(ValueError, match="division by zero"):
        divide(1, 0)


def test_mypy_strict_no_errors():
    result = subprocess.run(
        [sys.executable, "-m", "mypy", "--strict", "src/"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"mypy failed:\n{result.stdout}\n{result.stderr}"


def test_ruff_check_no_errors():
    result = subprocess.run(
        [sys.executable, "-m", "ruff", "check", "src/"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"ruff failed:\n{result.stdout}\n{result.stderr}"