"""Core arithmetic module with type annotations."""


def add(a: float, b: float) -> float:
    """Return the sum of a and b."""
    return float(a + b)


def subtract(a: float, b: float) -> float:
    """Return the difference of a and b."""
    return float(a - b)


def multiply(a: float, b: float) -> float:
    """Return the product of a and b."""
    return float(a * b)


def divide(a: float, b: float) -> float:
    """Return the quotient of a divided by b.

    Raises:
        ValueError: If b is zero.
    """
    if b == 0:
        raise ValueError("division by zero")
    return float(a / b)

