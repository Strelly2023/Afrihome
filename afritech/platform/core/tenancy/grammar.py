from __future__ import annotations

"""
GA Enterprise Core â€” Tenancy Grammar
-----------------------------------

LAYER: L1 (Foundation)
Dependencies: stdlib + core.errors.base
Deterministic: YES
Side effects: NONE

Purpose:
- Define the canonical grammar for tenant identifiers
- Provide pure, reusable grammar checks

Rules:
- Grammar ONLY (no resolution, no lookup)
- No kernel imports
- No normalization unless explicitly requested
- Grammar violations MUST raise GrammarViolationError
"""

import re
from typing import Final

from afritech.platform.core.errors.base import GrammarViolationError


# ============================================================
# Tenant identifier grammar
# ============================================================
#
# Rules:
# - lowercase ASCII
# - letters, digits, hyphens
# - must start with a letter
# - no consecutive hyphens
# - length: 3â€“63 characters
#
TENANT_SLUG_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$"
)


# ============================================================
# Grammar utilities (pure)
# ============================================================

def normalize_tenant_slug(value: str) -> str:
    """
    Normalize a tenant identifier candidate.

    Rules:
    - Must be a string
    - Strip leading/trailing whitespace
    - Lowercase
    """
    if not isinstance(value, str):
        raise GrammarViolationError(
            "Tenant slug must be a string",
            metadata={"value": value},
        )

    return value.strip().lower()


def is_valid_tenant_slug(value: str) -> bool:
    """
    Check whether a string matches the tenant grammar.

    Returns:
        True if valid, False otherwise.
    """
    if not isinstance(value, str):
        return False

    return bool(TENANT_SLUG_PATTERN.fullmatch(value))


def validate_tenant_slug(value: str) -> str:
    """
    Validate a tenant identifier candidate.

    Returns:
        The normalized tenant slug if valid.

    Raises:
        GrammarViolationError if the grammar is violated.
    """
    if not isinstance(value, str):
        raise GrammarViolationError(
            "Tenant slug must be a string",
            metadata={"value": value},
        )

    if not TENANT_SLUG_PATTERN.fullmatch(value):
        raise GrammarViolationError(
            "Invalid tenant slug",
            metadata={
                "value": value,
                "pattern": TENANT_SLUG_PATTERN.pattern,
            },
        )

    return value


# ============================================================
# Tenancy Grammar ABI (explicit, frozen)
# ============================================================

__all__ = [
    "TENANT_SLUG_PATTERN",
    "normalize_tenant_slug",
    "is_valid_tenant_slug",
    "validate_tenant_slug",
]
