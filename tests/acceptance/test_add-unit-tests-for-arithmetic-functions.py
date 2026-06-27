"""
Acceptance tests for the task: Add unit tests for arithmetic functions.

These tests validate that:
1. tests/test_calc.py exists and is discoverable by pytest.
2. The tests cover add, subtract, multiply, and divide with positive inputs.
3. A test verifies that divide raises ValueError on zero divisor.
4. Edge cases (negative numbers, zero) are covered.
5. `pytest` runs all tests and they pass.
6. `ruff check tests/` produces no errors.
7. `mypy --strict tests/` produces no errors.
"""

import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
TEST_CALC_PATH = REPO_ROOT / "tests" / "test_calc.py"


def run_command(
    cmd: list[str], cwd: Path | None = None
) -> subprocess.CompletedProcess[str]:
    """Run a command and return the completed process result."""
    return subprocess.run(
        cmd,
        cwd=cwd or REPO_ROOT,
        capture_output=True,
        text=True,
    )


def test_test_calc_file_exists() -> None:
    """Acceptance criterion 1: tests/test_calc.py exists."""
    assert TEST_CALC_PATH.exists(), f"Expected file at {TEST_CALC_PATH}"
    assert TEST_CALC_PATH.is_file(), f"{TEST_CALC_PATH} is not a regular file"


def test_test_calc_is_discoverable_by_pytest() -> None:
    """Acceptance criterion 1: tests/test_calc.py is discoverable by pytest."""
    result = run_command(
        [sys.executable, "-m", "pytest", "--collect-only", "-q", str(TEST_CALC_PATH)]
    )
    assert result.returncode == 0, (
        f"pytest could not collect tests from {TEST_CALC_PATH}\n"
        f"stdout: {result.stdout}\nstderr: {result.stderr}"
    )
    # There should be at least one test collected
    lines = [
        line.strip()
        for line in result.stdout.splitlines()
        if "::" in line and line.strip()
    ]
    assert len(lines) > 0, "No tests were collected from tests/test_calc.py"


def test_positive_input_tests_exist() -> None:
    """Acceptance criterion 2: Tests cover add, subtract, multiply, divide with positive inputs."""
    result = run_command(
        [sys.executable, "-m", "pytest", "--collect-only", "-q", str(TEST_CALC_PATH)]
    )
    assert result.returncode == 0, result.stderr

    collected = result.stdout.lower()
    # Check that test names or node ids reference all four functions with positive inputs
    assert "add" in collected, "No test referencing 'add' was found."
    assert "subtract" in collected, "No test referencing 'subtract' was found."
    assert "multiply" in collected, "No test referencing 'multiply' was found."
    assert "divide" in collected, "No test referencing 'divide' was found."


def test_divide_zero_divisor_raises_value_error() -> None:
    """Acceptance criterion 3: A test verifies divide raises ValueError on zero divisor."""
    content = TEST_CALC_PATH.read_text() if TEST_CALC_PATH.exists() else ""
    assert "ValueError" in content, (
        "tests/test_calc.py does not reference ValueError for zero divisor case."
    )
    assert "divide" in content, (
        "tests/test_calc.py does not reference divide function."
    )

    # Run the test suite and confirm divide-by-zero test passes
    result = run_command(
        [sys.executable, "-m", "pytest", str(TEST_CALC_PATH), "-v", "-k", "divide"]
    )
    assert result.returncode == 0, (
        f"Divide-related tests did not pass.\nstdout: {result.stdout}\nstderr: {result.stderr}"
    )


def test_edge_cases_covered() -> None:
    """Acceptance criterion 4: Edge cases (negative numbers, zero) are covered."""
    content = TEST_CALC_PATH.read_text() if TEST_CALC_PATH.exists() else ""
    content_lower = content.lower()

    # Check for references to negative numbers
    assert "negative" in content_lower or "-" in content, (
        "No test referencing negative numbers found in tests/test_calc.py."
    )
    # Check for references to zero
    assert "zero" in content_lower or "0" in content, (
        "No test referencing zero found in tests/test_calc.py."
    )

    # Run all tests to ensure edge case tests pass
    result = run_command([sys.executable, "-m", "pytest", str(TEST_CALC_PATH), "-v"])
    assert result.returncode == 0, (
        f"Edge case tests did not pass.\nstdout: {result.stdout}\nstderr: {result.stderr}"
    )


def test_pytest_runs_all_tests_and_passes() -> None:
    """Acceptance criterion 5: `pytest` runs all tests and they pass."""
    result = run_command([sys.executable, "-m", "pytest", str(TEST_CALC_PATH)])
    assert result.returncode == 0, (
        f"pytest did not pass all tests.\nstdout: {result.stdout}\nstderr: {result.stderr}"
    )
    # Confirm there is at least one passing test
    assert "passed" in result.stdout, (
        f"No tests reported as passing.\nstdout: {result.stdout}\nstderr: {result.stderr}"
    )


def test_ruff_check_no_errors() -> None:
    """Acceptance criterion 6: `ruff check tests/` produces no errors."""
    result = run_command(
        [sys.executable, "-m", "ruff", "check", "tests/"]
    )
    if result.returncode != 0 and "No module named ruff" in result.stderr:
        # Try system ruff if python module not found
        result = run_command(["ruff", "check", "tests/"])
    assert result.returncode == 0, (
        f"ruff check tests/ produced errors.\nstdout: {result.stdout}\nstderr: {result.stderr}"
    )


def test_mypy_strict_no_errors() -> None:
    """Acceptance criterion 7: `mypy --strict tests/` produces no errors."""
    result = run_command(
        [sys.executable, "-m", "mypy", "--strict", "tests/"]
    )
    if result.returncode != 0 and "No module named mypy" in result.stderr:
        # Try system mypy if python module not found
        result = run_command(["mypy", "--strict", "tests/"])
    assert result.returncode == 0, (
        f"mypy --strict tests/ produced errors.\nstdout: {result.stdout}\nstderr: {result.stderr}"
    )