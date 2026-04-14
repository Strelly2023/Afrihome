from __future__ import annotations

"""
GA Enterprise Core â€” Policy Grammar
----------------------------------

LAYER: L2 (Pure Engine)
Dependencies: stdlib + core.errors.base
Deterministic: YES
Side effects: NONE
IO / Time / Network: NONE

Purpose:
- Define the canonical grammar for policy conditions
- Centralize supported operators for policy evaluation
- Provide pure validation and normalization helpers

Rules:
- Grammar ONLY (no evaluation, no persistence)
- No kernel or L1 foundation imports (except CoreError types)
- Uses primitive types exclusively
- Grammar violations MUST raise GrammarViolationError
"""

from typing import Final

from afritech.platform.core.errors.base import GrammarViolationError


# ============================================================
# Supported operators
# ============================================================

# Operators supported by policy conditions.
# Meanings:
# - eq:       attribute equals value
# - neq:      attribute not equal to value
# - in:       attribute is a member of a collection
# - not_in:   attribute is not a member of a collection
# - exists:   attribute key exists (value ignored)
OPERATORS: Final[set[str]] = {"eq", "neq", "in", "not_in", "exists"}


# ============================================================
# Validation helpers (pure)
# ============================================================

def validate_operator(operator: str) -> str:
    """
    Validate a policy operator.

    Returns:
        The normalized operator if valid.

    Raises:
        GrammarViolationError if the operator is invalid or unsupported.
    """
    if not isinstance(operator, str) or not operator.strip():
        raise GrammarViolationError(
            "Policy operator must be a non-empty string",
            metadata={"operator": operator},
        )

    value = operator.strip()

    if value not in OPERATORS:
        raise GrammarViolationError(
            "Unsupported policy operator",
            metadata={
                "operator": value,
                "supported": sorted(OPERATORS),
            },
        )

    return value


def validate_attribute(attribute: str) -> str:
    """
    Validate a policy attribute name.

    Returns:
        The normalized attribute if valid.

    Raises:
        GrammarViolationError if the attribute is invalid.
    """
    if not isinstance(attribute, str) or not attribute.strip():
        raise GrammarViolationError(
            "Policy attribute must be a non-empty string",
            metadata={"attribute": attribute},
        )

    return attribute.strip()


# ============================================================
# Policy Grammar ABI (explicit, frozen)
# ============================================================

__all__ = [
    "OPERATORS",
    "validate_operator",
    "validate_attribute",
]
