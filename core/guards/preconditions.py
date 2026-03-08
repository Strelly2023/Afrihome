"""
GA Enterprise Core — Preconditions (Deterministic Guards)
---------------------------------------------------------

LAYER: L3
Dependencies:
- core.errors (InvariantViolationError, ValidationError, AuthorizationError)
- core.kernel.invariants (assert_not_none)

Rules:
- Pure helpers
- Deterministic, no side effects
"""

from typing import Any, Type

from core.errors import (
    AuthorizationError,
    InvariantViolationError,
    ValidationError,
)
from core.kernel.invariants import assert_not_none


def require(
    condition: bool, message: str, *, error: Type[Exception] = InvariantViolationError
) -> None:
    """
    Enforce an arbitrary boolean precondition.
    On failure, raises the provided deterministic error type (defaults to InvariantViolationError).
    """
    if condition is not True:
        raise error(message)


def require_present(value: Any, name: str) -> None:
    """
    Require that a value is not None (delegates to kernel invariant).
    """
    assert_not_none(value, name)


def require_non_empty_str(value: str | None, name: str) -> None:
    """
    Require a non-empty, non-whitespace-only string.
    """
    if value is None or len(value.strip()) == 0:
        raise ValidationError(f"{name} must be a non-empty string")


def require_equal(a: Any, b: Any, message: str = "Values must be equal") -> None:
    """
    Require equality between two values (strict != check).
    """
    if a != b:
        raise InvariantViolationError(message)


def require_allowed(allowed: bool, message: str = "Access denied") -> None:
    """
    Require an authorization check to be true (deny-wins).
    """
    if not allowed:
        raise AuthorizationError(message)
