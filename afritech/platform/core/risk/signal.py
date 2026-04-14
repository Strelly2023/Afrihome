from __future__ import annotations

"""
GA Enterprise Core â€” Risk Signal
--------------------------------

LAYER: L2 (Pure Engine)
Dependencies: core.risk.grammar + core.errors.base + stdlib
Deterministic: YES
Side effects: NONE
IO / Time / Network: NONE

Purpose:
- Represent a single immutable risk signal
- Provide a typed, deterministic input to risk evaluation

Rules:
- Pure value object only
- No kernel dependencies
- No evaluation or scoring logic
- Structural invariants MUST raise ValidationError
"""

from dataclasses import dataclass
from typing import Optional

from afritech.platform.core.risk.grammar import validate_signal
from afritech.platform.core.errors.base import ValidationError


# ============================================================
# Risk Signal (pure value object)
# ============================================================

@dataclass(frozen=True, slots=True)
class RiskSignal:
    """
    Immutable risk signal.

    Attributes:
        name:
            Canonical risk signal name (e.g. "geo_mismatch").
        weight:
            Optional deterministic weight contribution for this signal.
            Interpretation is defined by the RiskEvaluator.
    """

    name: str
    weight: Optional[int] = None

    def __post_init__(self) -> None:
        # ----------------------------------------------------
        # Grammar validation (authoritative)
        # ----------------------------------------------------

        object.__setattr__(
            self,
            "name",
            validate_signal(self.name),
        )

        # ----------------------------------------------------
        # Structural validation
        # ----------------------------------------------------

        if self.weight is not None and not isinstance(self.weight, int):
            raise ValidationError(
                "weight must be an integer if provided",
                metadata={"weight": self.weight},
            )

        # NOTE:
        # Weight range semantics are intentionally unconstrained here.
        # Interpretation and aggregation rules live exclusively
        # in the RiskEvaluator.


# ============================================================
# Risk Signal ABI (explicit, frozen)
# ============================================================

__all__ = [
    "RiskSignal",
]
