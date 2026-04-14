from __future__ import annotations

"""
GA Enterprise Core â€” Consent Decision
------------------------------------

LAYER: L2 (Pure Engine)
Dependencies: core.errors.base + stdlib
Deterministic: YES
Side effects: NONE
IO / Time / Network: NONE

Purpose:
- Represent the outcome of consent evaluation
- Provide a deterministic, replay-safe consent decision

Rules:
- Pure value object only
- No kernel dependencies
- No persistence, mutation, or side effects
- Structural invariants MUST raise ValidationError
"""

from dataclasses import dataclass
from typing import Tuple

from afritech.platform.core.errors.base import ValidationError


# ============================================================
# Consent Decision (pure value object)
# ============================================================

@dataclass(frozen=True, slots=True)
class ConsentDecision:
    """
    Result of consent evaluation.

    Attributes:
        allowed:
            Whether processing is legally permitted.
        state:
            Final effective consent state
            ("granted", "revoked", or "expired").
        reasons:
            Ordered tuple of machine-readable reasons explaining
            why this decision was reached.
    """

    allowed: bool
    state: str
    reasons: Tuple[str, ...]

    def __post_init__(self) -> None:
        # ----------------------------------------------------
        # Structural validation (fail-fast, deterministic)
        # ----------------------------------------------------

        if not isinstance(self.allowed, bool):
            raise ValidationError(
                "allowed must be a boolean",
                metadata={"allowed": self.allowed},
            )

        if not isinstance(self.state, str) or not self.state.strip():
            raise ValidationError(
                "state must be a non-empty string",
                metadata={"state": self.state},
            )

        if not isinstance(self.reasons, tuple):
            raise ValidationError(
                "reasons must be a tuple",
                metadata={"reasons_type": type(self.reasons).__name__},
            )

        if any(
            not isinstance(reason, str) or not reason.strip()
            for reason in self.reasons
        ):
            raise ValidationError(
                "all reasons must be non-empty strings",
                metadata={
                    "invalid_reasons": [
                        reason
                        for reason in self.reasons
                        if not isinstance(reason, str) or not reason.strip()
                    ]
                },
            )


# ============================================================
# Consent Decision ABI (explicit, frozen)
# ============================================================

__all__ = [
    "ConsentDecision",
]
