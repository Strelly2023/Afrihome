from __future__ import annotations

"""
GA Enterprise Core â€” Quota Grammar
---------------------------------

LAYER: L2 (Pure Engine)
Dependencies: stdlib + core.errors.base
Deterministic: YES
Side effects: NONE
IO / Time / Network: NONE

Purpose:
- Define canonical grammar for quota units, scopes, and dimensions
- Centralize validation for quota definitions
- Ensure deterministic, replay-safe quota semantics

Rules:
- Grammar ONLY (no evaluation, no persistence)
- No kernel imports
- No L1 foundation imports (except CoreError types)
- Uses primitive types exclusively
- Grammar violations MUST raise GrammarViolationError
"""

from typing import Final

from afritech.platform.core.errors.base import GrammarViolationError


# ============================================================
# Canonical quota units
# ============================================================

# Unit represents *what* is being counted.
# Examples:
# - "requests"
# - "messages"
# - "bytes"
# - "operations"
UNITS: Final[set[str]] = {
    "requests",
    "operations",
    "messages",
    "bytes",
    "records",
}


# ============================================================
# Canonical quota scopes
# ============================================================

# Scope represents *who* the quota applies to.
# These are logical scopes only â€” no identity types inside L2.
SCOPES: Final[set[str]] = {
    "global",
    "tenant",
    "user",
    "service",
}


# ============================================================
# Canonical quota dimensions
# ============================================================

# Dimension represents *how usage is grouped*.
# Typical examples:
# - per day
# - per hour
# - per rolling window
DIMENSIONS: Final[set[str]] = {
    "total",           # no window, absolute cap
    "per_minute",
    "per_hour",
    "per_day",
    "rolling_window",
}


# ============================================================
# Validation helpers (pure)
# ============================================================

def validate_unit(unit: str) -> str:
    """
    Validate a quota unit.

    Returns:
        The normalized unit if valid.

    Raises:
        GrammarViolationError if the unit is invalid or unsupported.
    """
    if not isinstance(unit, str) or not unit.strip():
        raise GrammarViolationError(
            "Quota unit must be a non-empty string",
            metadata={"unit": unit},
        )

    value = unit.strip()

    if value not in UNITS:
        raise GrammarViolationError(
            "Unsupported quota unit",
            metadata={
                "unit": value,
                "supported": sorted(UNITS),
            },
        )

    return value


def validate_scope(scope: str) -> str:
    """
    Validate a quota scope.

    Returns:
        The normalized scope if valid.

    Raises:
        GrammarViolationError if the scope is invalid or unsupported.
    """
    if not isinstance(scope, str) or not scope.strip():
        raise GrammarViolationError(
            "Quota scope must be a non-empty string",
            metadata={"scope": scope},
        )

    value = scope.strip()

    if value not in SCOPES:
        raise GrammarViolationError(
            "Unsupported quota scope",
            metadata={
                "scope": value,
                "supported": sorted(SCOPES),
            },
        )

    return value


def validate_dimension(dimension: str) -> str:
    """
    Validate a quota dimension.

    Returns:
        The normalized dimension if valid.

    Raises:
        GrammarViolationError if the dimension is invalid or unsupported.
    """
    if not isinstance(dimension, str) or not dimension.strip():
        raise GrammarViolationError(
            "Quota dimension must be a non-empty string",
            metadata={"dimension": dimension},
        )

    value = dimension.strip()

    if value not in DIMENSIONS:
        raise GrammarViolationError(
            "Unsupported quota dimension",
            metadata={
                "dimension": value,
                "supported": sorted(DIMENSIONS),
            },
        )

    return value


# ============================================================
# Quota Grammar ABI (explicit, frozen)
# ============================================================

__all__ = [
    # Grammar sets
    "UNITS",
    "SCOPES",
    "DIMENSIONS",

    # Validators
    "validate_unit",
    "validate_scope",
    "validate_dimension",
]
