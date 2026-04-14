from __future__ import annotations

"""
GA Enterprise Core â€” Tenancy Invariants
--------------------------------------

LAYER: L1 (Foundation)
Dependencies: stdlib + core.errors.base
Deterministic: YES
Side effects: NONE

Purpose:
- Enforce strict tenant identifier grammar rules
- Prevent cross-tenant ambiguity at boundaries

Rules:
- Grammar-only validation
- No tenant lookup or resolution
- No IO or external references
- Grammar violations MUST raise GrammarViolationError
"""

import re

from afritech.platform.core.errors.base import GrammarViolationError


# ---------------------------------------------------------------------
# Tenant identifier grammar
# ---------------------------------------------------------------------
#
# Rules:
# - lowercase ASCII
# - letters, digits, hyphens
# - must start with a letter
# - length: 3â€“63 characters
#
_TENANT_ID_RE = re.compile(
    r"^[a-z][a-z0-9-]{2,62}$"
)


def normalize_tenant_id(raw: str) -> str:
    """
    Normalize a tenant identifier.

    Rules:
    - must be a string
    - strip whitespace
    - lowercase
    """
    if not isinstance(raw, str):
        raise GrammarViolationError(
            "tenant_id must be a string",
            metadata={"value": raw},
        )

    return raw.strip().lower()


def validate_tenant_id(raw: str) -> str:
    """
    Validate tenant identifier grammar.

    Returns:
        Normalized tenant_id string.

    Raises:
        GrammarViolationError on grammar violation.
    """
    normalized = normalize_tenant_id(raw)

    if not normalized:
        raise GrammarViolationError(
            "tenant_id cannot be empty",
            metadata={"value": raw},
        )

    if not _TENANT_ID_RE.fullmatch(normalized):
        raise GrammarViolationError(
            "tenant_id must start with a letter and contain only "
            "lowercase letters, digits, or hyphens (length 3â€“63)",
            metadata={
                "tenant_id": normalized,
                "pattern": _TENANT_ID_RE.pattern,
            },
        )

    return normalized


# ---------------------------------------------------------------------
# Public ABI (explicit, frozen)
# ---------------------------------------------------------------------

__all__ = [
    "normalize_tenant_id",
    "validate_tenant_id",
]
