import pytest
from hello_calc import add, subtract, multiply, divide

def test_add():
    assert add(1, 2) == 3
    assert add(-1, -2) == -3
    assert add(1.5, 2.5) == 4.0
    assert add(0, 0) == 0

def test_subtract():
    assert subtract(2, 1) == 1
    assert subtract(-1, -2) == 1
    assert subtract(2.5, 1.5) == 1.0
    assert subtract(0, 0) == 0

def test_multiply():
    assert multiply(2, 3) == 6
    assert multiply(-1, -2) == 2
    assert multiply(1.5, 2.0) == 3.0
    assert multiply(0, 5) == 0

def test_divide():
    assert divide(4, 2) == 2
    assert divide(-4, -2) == 2
    assert divide(5, 2) == 2.5
    with pytest.raises(ValueError):
        divide(1, 0)
