"""
GA Enterprise Core — Kernel Invariant Enforcement
-------------------------------------------------

LAYER: L0
Dependencies: core.errors only
Deterministic: YES
Side effects: NONE

Purpose:
- Replace raw `assert` statements
- Provide deterministic invariant failures
"""

from typing import Any

from core.errors import InvariantViolationError

# ============================================================
# Base Invariant
# ============================================================


def assert_invariant(condition: bool, message: str) -> None:
    """
    Enforces a deterministic invariant.

    Raises:
        InvariantViolationError if condition is False.
    """
    if not condition:
        raise InvariantViolationError(message)


# ============================================================
# Common Assertions
# ============================================================


def assert_not_none(value: Any, name: str) -> None:
    """
    Ensures a value is not None.
    """
    if value is None:
        raise InvariantViolationError(f"{name} must not be None")


def assert_true(condition: bool, message: str) -> None:
    """
    Alias for explicit boolean checks.
    """
    if condition is not True:
        raise InvariantViolationError(message)
