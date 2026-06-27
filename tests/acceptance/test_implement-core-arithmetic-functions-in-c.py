"""Acceptance tests for core arithmetic functions in calc.py."""
import pytest
import inspect
from typing import get_type_hints

try:
    from hello_calc.calc import add, subtract, multiply, divide
except ImportError:
    from src.hello_calc.calc import add, subtract, multiply, divide


def test_add_returns_correct_float():
    result = add(2, 3)
    assert result == 5.0
    assert isinstance(result, float)


def test_subtract_returns_correct_float():
    result = subtract(10, 4)
    assert result == 6.0
    assert isinstance(result, float)


def test_multiply_returns_correct_float():
    result = multiply(3, 4)
    assert result == 12.0
    assert isinstance(result, float)


def test_divide_returns_correct_float():
    result = divide(10, 2)
    assert result == 5.0
    assert isinstance(result, float)


def test_divide_by_zero_raises_value_error():
    with pytest.raises(ValueError) as exc_info:
        divide(1, 0)
    assert str(exc_info.value) == 'division by zero'


def test_functions_have_float_type_annotations():
    functions = [add, subtract, multiply, divide]
    
    for func in functions:
        hints = get_type_hints(func)
        params = inspect.signature(func).parameters
        
        assert 'a' in params, f"{func.__name__} should have parameter 'a'"
        assert 'b' in params, f"{func.__name__} should have parameter 'b'"
        assert hints.get('a') is float, f"{func.__name__} parameter 'a' should be annotated as float"
        assert hints.get('b') is float, f"{func.__name__} parameter 'b' should be annotated as float"
        assert hints.get('return') is float, f"{func.__name__} return type should be annotated as float"