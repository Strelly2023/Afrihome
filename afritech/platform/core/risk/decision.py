from __future__ import annotations

"""
GA Enterprise Core â€” Risk Decision
---------------------------------

LAYER: L2 (Pure Engine)
Dependencies: core.risk.grammar + core.errors.base + stdlib
Deterministic: YES
Side effects: NONE
IO / Time / Network: NONE

Purpose:
- Represent the outcome of risk evaluation
- Provide a deterministic, replay-safe risk score and band

Rules:
- Pure value object only
- No kernel dependencies
- No persistence, mutation, or side effects
- Structural invariants MUST raise ValidationError
"""

from dataclasses import dataclass
from typing import Tuple

from afritech.platform.core.risk.grammar import (
    validate_score,
    validate_band,
)
from afritech.platform.core.errors.base import ValidationError


# ============================================================
# Risk Decision (pure value object)
# ============================================================

@dataclass(frozen=True, slots=True)
class RiskDecision:
    """
    Result of risk evaluation.

    Attributes:
        score:
            Final numeric risk score.
        band:
            Coarse risk band derived from the score
            (e.g. "low", "medium", "high", "critical").
        reasons:
            Ordered tuple of machine-readable reasons
            explaining why this score/band was produced.
    """

    score: int
    band: str
    reasons: Tuple[str, ...]

    def __post_init__(self) -> None:
        # ----------------------------------------------------
        # Grammar validation (authoritative)
        # ----------------------------------------------------

        object.__setattr__(
            self,
            "score",
            validate_score(self.score),
        )

        object.__setattr__(
            self,
            "band",
            validate_band(self.band),
        )

        # ----------------------------------------------------
        # Structural validation
        # ----------------------------------------------------

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
# Risk Decision ABI (explicit, frozen)
# ============================================================

__all__ = [
    "RiskDecision",
]
