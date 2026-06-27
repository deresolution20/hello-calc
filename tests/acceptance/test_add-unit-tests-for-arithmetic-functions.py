"""Acceptance tests for the task: Add unit tests for arithmetic functions.

These tests verify that:
1. tests/test_calc.py exists and uses pytest.
2. The test suite covers add, subtract, multiply, and divide.
3. There is a test verifying that divide(1, 0) raises ValueError.
4. Tests include edge cases for negative numbers and floating-point inputs.
5. pytest runs all tests with zero failures.
"""

import os
import re
import subprocess
import sys
import textwrap

import pytest


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
TEST_CALC_PATH = os.path.join(PROJECT_ROOT, "tests", "test_calc.py")


def _read_file(path):
    """Read file content; return empty string if file does not exist."""
    if not os.path.isfile(path):
        return ""
    with open(path, "r") as f:
        return f.read()


def _run_pytest_on_test_calc():
    """Run pytest on tests/test_calc.py and return the CompletedProcess."""
    cmd = [sys.executable, "-m", "pytest", TEST_CALC_PATH, "-v", "--tb=short"]
    return subprocess.run(cmd, capture_output=True, text=True, cwd=PROJECT_ROOT)


def test_test_calc_file_exists():
    """AC 1: tests/test_calc.py exists."""
    assert os.path.isfile(TEST_CALC_PATH), (
        f"Expected file at {TEST_CALC_PATH} but it does not exist."
    )


def test_test_calc_uses_pytest():
    """AC 1: The test file is pytest-based (imports pytest or uses pytest features)."""
    content = _read_file(TEST_CALC_PATH)
    assert content, "tests/test_calc.py is empty or does not exist."
    assert "pytest" in content, "tests/test_calc.py does not reference pytest."


def test_suite_covers_add():
    """AC 2: Test suite covers the add function."""
    content = _read_file(TEST_CALC_PATH)
    assert re.search(r"def test.*add", content, re.IGNORECASE), (
        "No test function found for add."
    )


def test_suite_covers_subtract():
    """AC 2: Test suite covers the subtract function."""
    content = _read_file(TEST_CALC_PATH)
    assert re.search(r"def test.*subtract", content, re.IGNORECASE), (
        "No test function found for subtract."
    )


def test_suite_covers_multiply():
    """AC 2: Test suite covers the multiply function."""
    content = _read_file(TEST_CALC_PATH)
    assert re.search(r"def test.*multiply", content, re.IGNORECASE), (
        "No test function found for multiply."
    )


def test_suite_covers_divide():
    """AC 2: Test suite covers the divide function."""
    content = _read_file(TEST_CALC_PATH)
    assert re.search(r"def test.*divide", content, re.IGNORECASE), (
        "No test function found for divide."
    )


def test_divide_by_zero_raises_value_error():
    """AC 3: A test verifies that divide(1, 0) raises ValueError."""
    content = _read_file(TEST_CALC_PATH)
    # Look for a divide-by-zero test that expects ValueError
    has_divide_by_zero = (
        "divide" in content.lower()
        and "0" in content
        and "ValueError" in content
    )
    assert has_divide_by_zero, (
        "No test found verifying that divide by zero raises ValueError."
    )
    # More specific check: a test function mentioning divide and zero and ValueError
    # Search for pytest.raises(ValueError) near divide
    assert "ValueError" in content, "ValueError not mentioned in test file."
    assert re.search(r"divide\s*\(.+,\s*0\s*\)", content) or re.search(
        r"divide.*zero", content, re.IGNORECASE
    ), "No explicit divide(..., 0) or divide-by-zero reference found."


def test_includes_negative_number_edge_case():
    """AC 4: Tests include edge cases for negative numbers."""
    content = _read_file(TEST_CALC_PATH)
    # Check for negative number usage in tests
    assert re.search(r"-\d", content), (
        "No negative number inputs found in the test file."
    )


def test_includes_floating_point_edge_case():
    """AC 4: Tests include edge cases for floating-point inputs."""
    content = _read_file(TEST_CALC_PATH)
    # Check for floating-point number usage (e.g., 1.5, 2.0, 0.1)
    assert re.search(r"\d+\.\d+", content), (
        "No floating-point inputs found in the test file."
    )


def test_pytest_runs_all_tests_with_zero_failures():
    """AC 5: pytest runs all tests in tests/test_calc.py with zero failures."""
    result = _run_pytest_on_test_calc()
    combined = result.stdout + result.stderr
    # Check that pytest ran
    assert result.returncode == 0, (
        f"pytest did not pass with zero failures. Return code: {result.returncode}\n"
        f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )
    # Ensure at least one test was collected and passed
    assert "passed" in combined, (
        f"No passing tests reported by pytest.\n"
        f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )
    assert "failed" not in combined.lower() or "0 failed" in combined, (
        f"pytest reported failures.\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )