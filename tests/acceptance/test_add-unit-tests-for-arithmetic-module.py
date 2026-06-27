"""Acceptance tests for the arithmetic module in hello_calc.

These tests validate that hello_calc re-exports and correctly implements
add, subtract, multiply, and divide, covering normal values, negative
numbers, float results, and the division-by-zero error path.
"""
import pytest
from hello_calc import add, subtract, multiply, divide


def test_add_multiple_cases():
    assert add(1, 2) == 3
    assert add(-1, -1) == -2
    assert add(-1, 1) == 0
    assert add(0, 0) == 0
    assert add(1.5, 2.5) == 4.0


def test_subtract_multiple_cases():
    assert subtract(5, 3) == 2
    assert subtract(3, 5) == -2
    assert subtract(-5, -3) == -2
    assert subtract(-5, 3) == -8
    assert subtract(2.5, 1.0) == 1.5


def test_multiply_multiple_cases():
    assert multiply(2, 3) == 6
    assert multiply(-2, 3) == -6
    assert multiply(-2, -3) == 6
    assert multiply(0, 5) == 0
    assert multiply(1.5, 2) == 3.0


def test_divide_multiple_cases():
    assert divide(6, 3) == 2
    assert divide(5, 2) == 2.5
    assert divide(-6, 3) == -2
    assert divide(-6, -3) == 2
    assert divide(0, 5) == 0


def test_divide_by_zero_raises_value_error():
    with pytest.raises(ValueError):
        divide(1, 0)