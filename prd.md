# hello-calc: Simple Python Calculator Library

A tiny Python library that exposes basic arithmetic as a clean, type-annotated API.
This project exists to test the agentic build platform end-to-end.

## Task 1: Implement core arithmetic module

Implement `src/hello_calc/calc.py` with the following four functions:

```python
def add(a: float, b: float) -> float: ...
def subtract(a: float, b: float) -> float: ...
def multiply(a: float, b: float) -> float: ...
def divide(a: float, b: float) -> float: ...
```

- `add(a, b)` returns `a + b`
- `subtract(a, b)` returns `a - b`
- `multiply(a, b)` returns `a * b`
- `divide(a, b)` returns `a / b`; raises `ValueError("division by zero")` when `b == 0`

Also update `src/hello_calc/__init__.py` to re-export all four functions:
```python
from hello_calc.calc import add, divide, multiply, subtract

__all__ = ["add", "subtract", "multiply", "divide"]
```

### Acceptance criteria

1. `from hello_calc import add, subtract, multiply, divide` succeeds after `pip install -e .`
2. `add(2, 3)` returns `5.0`
3. `subtract(10, 4)` returns `6.0`
4. `multiply(3, 4)` returns `12.0`
5. `divide(10, 2)` returns `5.0`
6. `divide(1, 0)` raises `ValueError`
7. All four functions pass `mypy --strict`
8. `ruff check src/` produces no errors
