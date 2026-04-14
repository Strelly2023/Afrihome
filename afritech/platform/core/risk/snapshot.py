from __future__ import annotations

"""
GA Enterprise Core â€” Risk Snapshot
---------------------------------

LAYER: L2 (Pure Engine)
Dependencies: core.risk.signal + core.errors.base + stdlib
Deterministic: YES
Side effects: NONE
IO / Time / Network: NONE

Purpose:
- Represent an immutable snapshot of observed risk context
- Provide deterministic input to the Risk evaluation engine

Rules:
- Pure value object only
- No kernel dependencies
- No clocks, IO, or persistence
- Structural invariants MUST raise ValidationError
"""

from dataclasses import dataclass
from typing import Tuple

from afritech.platform.core.risk.signal import RiskSignal
from afritech.platform.core.errors.base import ValidationError


# ============================================================
# Risk Snapshot (pure value object)
# ============================================================

@dataclass(frozen=True, slots=True)
class RiskSnapshot:
    """
    Immutable snapshot of observed risk signals.

    Attributes:
        model_id:
            Identifier of the risk model this snapshot targets.
        signals:
            Tuple of observed RiskSignal instances at evaluation time.
    """

    model_id: str
    signals: Tuple[RiskSignal, ...]

    def __post_init__(self) -> None:
        # ----------------------------------------------------
        # Structural validation (fail-fast, deterministic)
        # ----------------------------------------------------

        if not isinstance(self.model_id, str) or not self.model_id.strip():
            raise ValidationError(
                "model_id must be a non-empty string",
                metadata={"model_id": self.model_id},
            )

        if not isinstance(self.signals, tuple):
            raise ValidationError(
                "signals must be a tuple",
                metadata={"signals_type": type(self.signals).__name__},
            )

        if any(not isinstance(signal, RiskSignal) for signal in self.signals):
            raise ValidationError(
                "all elements of signals must be RiskSignal instances",
                metadata={
                    "invalid_signals": [
                        type(signal).__name__
                        for signal in self.signals
                        if not isinstance(signal, RiskSignal)
                    ]
                },
            )


# ============================================================
# Risk Snapshot ABI (explicit, frozen)
# ============================================================

__all__ = [
    "RiskSnapshot",
]
