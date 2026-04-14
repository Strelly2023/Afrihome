"""
GA Enterprise Core â€” Kernel Invariant Enforcement
-------------------------------------------------

LAYER: L0 (Kernel)
Dependencies: stdlib only
Deterministic: YES
Side effects: NONE

Purpose:
- Replace raw `assert` statements
- Provide deterministic invariant failures
"""

from typing import Any


# ============================================================
# Base invariant
# ============================================================

def assert_invariant(condition: bool, message: str) -> None:
    """
    Enforce a deterministic invariant.

    Raises:
        RuntimeError: if the invariant fails.
    """
    if not condition:
        raise RuntimeError(message)


# ============================================================
# Common kernel assertions
# ============================================================

def assert_not_none(value: Any, name: str) -> None:
    """
    Ensure a value is not None.

    Args:
        value: Value to check.
        name: Logical name for error message.
    """
    if value is None:
        raise RuntimeError(f"{name} must not be None")


def assert_true(condition: bool, message: str) -> None:
    """
    Explicit boolean invariant.

    Raises:
        RuntimeError: if condition is False.
    """
    if not condition:
        raise RuntimeError(message)
__all__ = [
    "assert_invariant",
    "assert_not_none",
    "assert_true",
]
