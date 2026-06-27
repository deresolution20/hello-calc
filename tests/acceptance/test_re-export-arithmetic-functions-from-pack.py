"""Acceptance tests for re-exporting arithmetic functions from hello_calc package __init__.

These tests validate that:
1. `from hello_calc import add, subtract, multiply, divide` succeeds
2. `__all__` is set to the expected list of function names
3. `ruff check src/` produces no errors
"""

import subprocess
import sys


def test_can_import_all_four_functions_from_package():
    """Acceptance criterion 1: `from hello_calc import add, subtract, multiply, divide` succeeds."""
    from hello_calc import add, subtract, multiply, divide

    # Verify each imported name is callable
    assert callable(add)
    assert callable(subtract)
    assert callable(multiply)
    assert callable(divide)

    # Verify they actually work as arithmetic functions
    assert add(1, 2) == 3
    assert subtract(5, 3) == 2
    assert multiply(4, 6) == 24
    assert divide(10, 2) == 5


def test_all_contains_expected_names():
    """Acceptance criterion 2: `__all__` is set to ["add", "subtract", "multiply", "divide"]."""
    import hello_calc

    assert hasattr(hello_calc, "__all__")
    assert hello_calc.__all__ == ["add", "subtract", "multiply", "divide"]


def test_ruff_check_src_produces_no_errors():
    """Acceptance criterion 3: `ruff check src/` produces no errors."""
    result = subprocess.run(
        ["ruff", "check", "src/"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"ruff check src/ failed with exit code {result.returncode}.\n"
        f"stdout:\n{result.stdout}\n"
        f"stderr:\n{result.stderr}"
    )