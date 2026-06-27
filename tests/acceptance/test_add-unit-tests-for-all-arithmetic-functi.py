"""
Acceptance tests for the task: Add unit tests for all arithmetic functions.

These tests validate that:
1. tests/test_calc.py exists and is discovered by pytest
2. Tests cover add, subtract, multiply, and divide functions
3. Tests verify divide by zero raises ValueError
4. Tests verify float return types
5. All tests pass when run with pytest
"""
import os
import subprocess
import sys
import textwrap

import pytest


# ---------------------------------------------------------------------------
# Criterion 1: tests/test_calc.py exists and is discovered by pytest
# ---------------------------------------------------------------------------

def test_test_calc_file_exists():
    """tests/test_calc.py must exist in the repository root."""
    # The acceptance test is located under tests/acceptance/, so the
    # repository root is two levels up from this file's directory.
    here = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.abspath(os.path.join(here, "..", ".."))
    test_file = os.path.join(repo_root, "tests", "test_calc.py")
    assert os.path.isfile(test_file), f"Expected {test_file} to exist"


def test_test_calc_discovered_by_pytest():
    """Running pytest on tests/test_calc.py must collect at least one test."""
    here = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.abspath(os.path.join(here, "..", ".."))
    test_file = os.path.join(repo_root, "tests", "test_calc.py")

    result = subprocess.run(
        [sys.executable, "-m", "pytest", test_file, "--collect-only", "-q"],
        capture_output=True,
        text=True,
        cwd=repo_root,
    )
    assert result.returncode == 0, result.stderr
    # Collect-only output lists each test; ensure at least one item collected
    assert "no tests collected" not in result.stdout.lower()
    # There should be at least 4 test items (add, subtract, multiply, divide)
    lines = [l for l in result.stdout.splitlines() if "::" in l]
    assert len(lines) >= 4, f"Expected >=4 tests, got {len(lines)}: {lines}"


# ---------------------------------------------------------------------------
# Criterion 2 & 4: Functions work and return floats
# ---------------------------------------------------------------------------

def test_add_returns_float_positive():
    from hello_calc import add
    result = add(2, 3)
    assert result == 5.0
    assert isinstance(result, float)


def test_add_returns_float_negative():
    from hello_calc import add
    result = add(-1, -4)
    assert result == -5.0
    assert isinstance(result, float)


def test_add_with_zero():
    from hello_calc import add
    result = add(0, 5)
    assert result == 5.0
    assert isinstance(result, float)


def test_add_float_inputs():
    from hello_calc import add
    result = add(1.5, 2.5)
    assert result == 4.0
    assert isinstance(result, float)


def test_subtract_returns_float():
    from hello_calc import subtract
    result = subtract(10, 3)
    assert result == 7.0
    assert isinstance(result, float)


def test_subtract_negative():
    from hello_calc import subtract
    result = subtract(-2, -5)
    assert result == 3.0
    assert isinstance(result, float)


def test_multiply_returns_float():
    from hello_calc import multiply
    result = multiply(3, 4)
    assert result == 12.0
    assert isinstance(result, float)


def test_multiply_with_zero():
    from hello_calc import multiply
    result = multiply(0, 100)
    assert result == 0.0
    assert isinstance(result, float)


def test_multiply_negative():
    from hello_calc import multiply
    result = multiply(-3, 5)
    assert result == -15.0
    assert isinstance(result, float)


def test_divide_returns_float():
    from hello_calc import divide
    result = divide(10, 2)
    assert result == 5.0
    assert isinstance(result, float)


def test_divide_float_result():
    from hello_calc import divide
    result = divide(5, 2)
    assert result == 2.5
    assert isinstance(result, float)


# ---------------------------------------------------------------------------
# Criterion 3: divide by zero raises ValueError
# ---------------------------------------------------------------------------

def test_divide_by_zero_raises_value_error():
    from hello_calc import divide
    with pytest.raises(ValueError):
        divide(10, 0)


# ---------------------------------------------------------------------------
# Criterion 5: All tests pass when run with pytest
# ---------------------------------------------------------------------------

def test_all_unit_tests_pass():
    """Running pytest on tests/test_calc.py must exit 0."""
    here = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.abspath(os.path.join(here, "..", ".."))
    test_file = os.path.join(repo_root, "tests", "test_calc.py")

    result = subprocess.run(
        [sys.executable, "-m", "pytest", test_file, "-q"],
        capture_output=True,
        text=True,
        cwd=repo_root,
    )
    assert result.returncode == 0, (
        f"pytest exited with {result.returncode}\nSTDOUT:\n{result.stdout}\n"
        f"STDERR:\n{result.stderr}"
    )