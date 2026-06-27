"""Acceptance tests for the core arithmetic module implementation.

These tests validate:
- Existence of calc.py with add, subtract, multiply, divide functions
- Correct return values for add, subtract, multiply, divide
- ValueError raised by divide when dividing by zero
- Functions are re-exported from hello_calc package
- __all__ is defined with all four function names
"""

import importlib
import os
from pathlib import Path

import pytest


def test_calc_py_exists_with_required_functions():
    """Acceptance Criterion 1: calc.py exists with add, subtract, multiply, divide."""
    # Find the project root by looking for setup.py or pyproject.toml
    test_file = Path(__file__).resolve()
    project_root = test_file
    while project_root.parent != project_root:
        for marker in ("pyproject.toml", "setup.py", "setup.cfg"):
            if (project_root / marker).exists():
                break
        else:
            project_root = project_root.parent
            continue
        break

    calc_path = project_root / "src" / "hello_calc" / "calc.py"
    assert calc_path.exists(), f"calc.py not found at {calc_path}"

    spec = importlib.util.spec_from_file_location("hello_calc.calc", calc_path)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    assert hasattr(module, "add"), "calc.py must define 'add'"
    assert hasattr(module, "subtract"), "calc.py must define 'subtract'"
    assert hasattr(module, "multiply"), "calc.py must define 'multiply'"
    assert hasattr(module, "divide"), "calc.py must define 'divide'"
    assert callable(module.add)
    assert callable(module.subtract)
    assert callable(module.multiply)
    assert callable(module.divide)


def test_add_returns_correct_value():
    """Acceptance Criterion 2: add(2, 3) returns 5.0."""
    from hello_calc.calc import add

    result = add(2, 3)
    assert result == 5.0
    assert isinstance(result, float)


def test_subtract_returns_correct_value():
    """Acceptance Criterion 3: subtract(10, 4) returns 6.0."""
    from hello_calc.calc import subtract

    result = subtract(10, 4)
    assert result == 6.0
    assert isinstance(result, float)


def test_multiply_returns_correct_value():
    """Acceptance Criterion 4: multiply(3, 4) returns 12.0."""
    from hello_calc.calc import multiply

    result = multiply(3, 4)
    assert result == 12.0
    assert isinstance(result, float)


def test_divide_returns_correct_value():
    """Acceptance Criterion 5: divide(10, 2) returns 5.0."""
    from hello_calc.calc import divide

    result = divide(10, 2)
    assert result == 5.0
    assert isinstance(result, float)


def test_divide_by_zero_raises_value_error():
    """Acceptance Criterion 6: divide(1, 0) raises ValueError with message 'division by zero'."""
    from hello_calc.calc import divide

    with pytest.raises(ValueError) as exc_info:
        divide(1, 0)
    assert str(exc_info.value) == "division by zero"


def test_functions_importable_from_package():
    """Acceptance Criterion 7: from hello_calc import add, subtract, multiply, divide succeeds."""
    from hello_calc import add, subtract, multiply, divide

    assert callable(add)
    assert callable(subtract)
    assert callable(multiply)
    assert callable(divide)

    # Verify they actually work
    assert add(2, 3) == 5.0
    assert subtract(10, 4) == 6.0
    assert multiply(3, 4) == 12.0
    assert divide(10, 2) == 5.0


def test_all_is_defined_with_all_four_function_names():
    """Acceptance Criterion 8: __all__ is defined in __init__.py with all four function names."""
    import hello_calc

    assert hasattr(hello_calc, "__all__"), "__all__ must be defined in __init__.py"
    assert "add" in hello_calc.__all__, "__all__ must contain 'add'"
    assert "subtract" in hello_calc.__all__, "__all__ must contain 'subtract'"
    assert "multiply" in hello_calc.__all__, "__all__ must contain 'multiply'"
    assert "divide" in hello_calc.__all__, "__all__ must contain 'divide'"