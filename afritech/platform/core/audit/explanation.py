from __future__ import annotations

"""
GA Enterprise Core â€” Audit Explanation
-------------------------------------

LAYER: L2 (Pure Engine)
Dependencies: core.errors.base + stdlib
Deterministic: YES
Side effects: NONE
IO / Time / Network: NONE

Purpose:
- Represent a human-readable explanation of an authorization decision
- Provide structured, replay-safe explanation data for higher layers

Rules:
- Pure value object
- No identity, tenancy, persistence, or formatting concerns
- No kernel dependencies
- Structural invariants MUST raise ValidationError
"""

from dataclasses import dataclass
from typing import Tuple

from afritech.platform.core.errors.base import ValidationError


# ============================================================
# Audit Explanation (pure value object)
# ============================================================

@dataclass(frozen=True, slots=True)
class AuditExplanation:
    """
    Human-readable explanation of an authorization decision.

    Attributes:
        summary:
            Short, high-level explanation
            (e.g. "Denied by policy rule").
        details:
            Ordered list of detailed explanation lines that expand
            on the decision (e.g. rule matches, condition failures).
    """

    summary: str
    details: Tuple[str, ...]

    def __post_init__(self) -> None:
        # ----------------------------------------------------
        # Structural validation (fail-fast, deterministic)
        # ----------------------------------------------------

        if not isinstance(self.summary, str) or not self.summary.strip():
            raise ValidationError(
                "summary must be a non-empty string",
                metadata={"summary": self.summary},
            )

        if not isinstance(self.details, tuple):
            raise ValidationError(
                "details must be a tuple",
                metadata={"details_type": type(self.details).__name__},
            )

        if any(not isinstance(detail, str) for detail in self.details):
            raise ValidationError(
                "all elements of details must be strings",
                metadata={
                    "invalid_details": [
                        detail
                        for detail in self.details
                        if not isinstance(detail, str)
                    ]
                },
            )


# ============================================================
# Audit Explanation ABI (explicit, frozen)
# ============================================================

__all__ = [
    "AuditExplanation",
]
