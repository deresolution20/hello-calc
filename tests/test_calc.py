import pytest
from hello_calc import add, subtract, multiply, divide

def test_add():
    assert add(2, 3) == 5.0
    assert add(-1, -1) == -2.0
    assert add(-1, 1) == 0.0
    assert add(0, 0) == 0.0
    assert isinstance(add(2, 3), float)

def test_subtract():
    assert subtract(5, 3) == 2.0
    assert subtract(-1, -1) == 0.0
    assert subtract(-1, 1) == -2.0
    assert subtract(0, 0) == 0.0
    assert isinstance(subtract(2, 3), float)

def test_multiply():
    assert multiply(2, 3) == 6.0
    assert multiply(-1, -1) == 1.0
    assert multiply(-1, 1) == -1.0
    assert multiply(0, 0) == 0.0
    assert isinstance(multiply(2, 3), float)

def test_divide():
    assert divide(6, 3) == 2.0
    assert divide(-6, -3) == 2.0
    assert divide(-6, 3) == -2.0
    assert divide(0, 1) == 0.0
    assert isinstance(divide(2, 3), float)

def test_divide_by_zero():
    with pytest.raises(ValueError):
        divide(1, 0)
