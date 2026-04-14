from __future__ import annotations

"""
GA Enterprise Core â€” Risk Definition
-----------------------------------

LAYER: L2 (Pure Engine)
Dependencies: core.risk.grammar + core.risk.signal + core.errors.base + stdlib
Deterministic: YES
Side effects: NONE
IO / Time / Network: NONE

Purpose:
- Represent an immutable risk scoring definition
- Describe how risk signals contribute to a total risk score

Rules:
- Pure value object only
- No kernel dependencies
- No evaluation or aggregation logic
- Structural invariants MUST raise ValidationError
"""

from dataclasses import dataclass
from typing import Tuple

from afritech.platform.core.risk.signal import RiskSignal
from afritech.platform.core.risk.grammar import (
    validate_score,
    validate_band,
)
from afritech.platform.core.errors.base import ValidationError


# ============================================================
# Risk Definition (pure value object)
# ============================================================

@dataclass(frozen=True, slots=True)
class RiskDefinition:
    """
    Immutable risk scoring definition.

    Attributes:
        model_id:
            Logical identifier of the risk model
            (e.g. "default-auth-risk").
        base_score:
            Baseline risk score before signals are applied.
        signals:
            Tuple of RiskSignal entries that may contribute
            to the final score.
        band_thresholds:
            Ordered tuple of (band, minimum_score) pairs,
            defining how numeric scores map to bands.
    """

    model_id: str
    base_score: int
    signals: Tuple[RiskSignal, ...]
    band_thresholds: Tuple[tuple[str, int], ...]

    def __post_init__(self) -> None:
        # ----------------------------------------------------
        # Structural validation
        # ----------------------------------------------------

        if not isinstance(self.model_id, str) or not self.model_id.strip():
            raise ValidationError(
                "model_id must be a non-empty string",
                metadata={"model_id": self.model_id},
            )

        # Base score validation (delegated to grammar)
        validate_score(self.base_score)

        if not isinstance(self.signals, tuple):
            raise ValidationError(
                "signals must be a tuple",
                metadata={"signals_type": type(self.signals).__name__},
            )

        if any(not isinstance(s, RiskSignal) for s in self.signals):
            raise ValidationError(
                "all elements of signals must be RiskSignal instances",
                metadata={
                    "invalid_signals": [
                        type(s).__name__
                        for s in self.signals
                        if not isinstance(s, RiskSignal)
                    ]
                },
            )

        if not isinstance(self.band_thresholds, tuple):
            raise ValidationError(
                "band_thresholds must be a tuple",
                metadata={
                    "band_thresholds_type":
                        type(self.band_thresholds).__name__
                },
            )

        if not self.band_thresholds:
            raise ValidationError(
                "band_thresholds must contain at least one entry",
            )

        # ----------------------------------------------------
        # Band threshold validation (ordered, deterministic)
        # ----------------------------------------------------

        last_score: int | None = None
        for band, score in self.band_thresholds:
            validate_band(band)
            validate_score(score)

            if last_score is not None and score < last_score:
                raise ValidationError(
                    "band_thresholds must be ordered by increasing score",
                    metadata={
                        "previous_score": last_score,
                        "current_score": score,
                    },
                )

            last_score = score


# ============================================================
# Risk Definition ABI (explicit, frozen)
# ============================================================

__all__ = [
    "RiskDefinition",
]
