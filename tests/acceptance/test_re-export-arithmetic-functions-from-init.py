"""
Acceptance tests for re-exporting arithmetic functions from hello_calc/__init__.py.

These tests validate that:
1. The four arithmetic functions can be imported directly from hello_calc.
2. Each function is callable.
3. __all__ is defined as ['add', 'subtract', 'multiply', 'divide'].
"""

import hello_calc


def test_import_add_succeeds():
    from hello_calc import add
    assert add is not None


def test_import_subtract_succeeds():
    from hello_calc import subtract
    assert subtract is not None


def test_import_multiply_succeeds():
    from hello_calc import multiply
    assert multiply is not None


def test_import_divide_succeeds():
    from hello_calc import divide
    assert divide is not None


def test_add_is_callable():
    from hello_calc import add
    assert callable(add)


def test_subtract_is_callable():
    from hello_calc import subtract
    assert callable(subtract)


def test_multiply_is_callable():
    from hello_calc import multiply
    assert callable(multiply)


def test_divide_is_callable():
    from hello_calc import divide
    assert callable(divide)


def test_all_functions_callable_via_module_attribute():
    assert callable(hello_calc.add)
    assert callable(hello_calc.subtract)
    assert callable(hello_calc.multiply)
    assert callable(hello_calc.divide)


def test_all_is_defined():
    assert hasattr(hello_calc, "__all__")


def test_all_contains_expected_functions():
    assert hello_calc.__all__ == ["add", "subtract", "multiply", "divide"]


def test_all_is_list():
    assert isinstance(hello_calc.__all__, list)
    assert set(hello_calc.__all__) == {"add", "subtract", "multiply", "divide"}