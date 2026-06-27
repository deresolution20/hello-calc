"""Acceptance tests for adding unit tests for arithmetic functions.

These tests verify that:
1. All four arithmetic functions (add, subtract, multiply, divide) are
   covered with positive test cases.
2. divide(1, 0) raises ValueError for the divide-by-zero case.
3. Functions are imported via `from hello_calc import ...` at the package
   level, confirming the re-export works.
4. The tests are runnable with pytest and pass.
"""
import pytest

from hello_calc import add, subtract, multiply, divide


# ---------------------------------------------------------------------------
# Criterion 2: Tests cover add, subtract, multiply, and divide
# ---------------------------------------------------------------------------

def test_add_two_positive_numbers():
    assert add(2, 3) == 5


def test_add_negative_numbers():
    assert add(-4, -6) == -10


def test_add_mixed_sign_numbers():
    assert add(-4, 10) == 6


def test_subtract_two_positive_numbers():
    assert subtract(10, 4) == 6


def test_subtract_resulting_in_negative():
    assert subtract(3, 7) == -4


def test_subtract_equal_numbers():
    assert subtract(5, 5) == 0


def test_multiply_two_positive_numbers():
    assert multiply(3, 4) == 12


def test_multiply_by_zero():
    assert multiply(7, 0) == 0


def test_multiply_negative_numbers():
    assert multiply(-3, -4) == 12


def test_divide_evenly_divisible():
    assert divide(10, 2) == 5


def test_divide_with_float_result():
    assert divide(7, 2) == 3.5


def test_divide_negative_by_positive():
    assert divide(-8, 4) == -2


# ---------------------------------------------------------------------------
# Criterion 3: At least one test asserts divide(1, 0) raises ValueError
# ---------------------------------------------------------------------------

def test_divide_by_zero_raises_value_error():
    with pytest.raises(ValueError):
        divide(1, 0)


def test_divide_by_zero_raises_value_error_message_check():
    with pytest.raises(ValueError, match=r"(?i).*zero.*|.*div.*"):
        divide(1, 0)


# ---------------------------------------------------------------------------
# Criterion 4: Tests import functions via `from hello_calc import ...`
# ---------------------------------------------------------------------------

def test_functions_are_importable_from_package_level():
    """Verify that add, subtract, multiply, divide exist on the hello_calc
    package, confirming re-export at the package level."""
    import hello_calc

    assert callable(getattr(hello_calc, "add"))
    assert callable(getattr(hello_calc, "subtract"))
    assert callable(getattr(hello_calc, "multiply"))
    assert callable(getattr(hello_calc, "divide"))


def test_imported_functions_are_the_same_objects_as_package_attributes():
    """The names imported via `from hello_calc import ...` must be the same
    objects exposed on the package."""
    import hello_calc

    assert add is hello_calc.add
    assert subtract is hello_calc.subtract
    assert multiply is hello_calc.multiply
    assert divide is hello_calc.divide


# ---------------------------------------------------------------------------
# Criterion 1: Running pytest executes all tests and they pass
# (Implicitly satisfied when this module is collected and all tests pass.)
# ---------------------------------------------------------------------------

def test_pytest_can_run_all_arithmetic_tests():
    """Smoke test ensuring the arithmetic functions produce expected results
    in a single combined assertion, confirming pytest execution."""
    assert add(1, 2) == 3
    assert subtract(5, 3) == 2
    assert multiply(2, 3) == 6
    assert divide(8, 2) == 4