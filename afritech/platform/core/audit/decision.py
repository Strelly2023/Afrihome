from __future__ import annotations

"""
GA Enterprise Core â€” Audit Decision
----------------------------------

LAYER: L2 (Pure Projection Layer)
Dependencies:
- core.audit.trace
- core.decision.decision
- core.typing.enums
- core.errors.base
- stdlib only

Deterministic: YES
Side effects: NONE
IO / Time / Network: NONE

Purpose:
- Represent the final, immutable outcome of an authorization decision
- Capture factual information needed for audit, replay, and explainability
- Project core decision semantics without reâ€‘interpreting them

Rules:
- Pure value object
- NO kernel dependencies
- NO IO, persistence, or identity mapping
- NO decision logic or precedence
- Structural invariants MUST raise ValidationError
- Enums are the sole semantic authority
"""

from dataclasses import dataclass
from typing import Tuple

from afritech.platform.core.audit.trace import AuditTrace
from afritech.platform.core.decision.decision import Decision
from afritech.platform.core.typing.enums import EngineId, DecisionVerdictType
from afritech.platform.core.errors.base import ValidationError


# ============================================================
# Audit Decision (pure projection value object)
# ============================================================

@dataclass(frozen=True, slots=True)
class AuditDecision:
    """
    Immutable audit representation of a decision outcome.

    Attributes:
        allowed:
            Final authorization result (projection of Decision.verdict).
        engine:
            Engine context of the final decision (EngineId).
        verdict:
            Canonical decision verdict (DecisionVerdictType).
        reason:
            Humanâ€‘ or machineâ€‘readable summary of the outcome.
        traces:
            Ordered set of factual audit traces explaining why
            the decision was reached.

    NOTES:
    - This object MUST NOT decide anything.
    - It MUST faithfully reflect a core Decision.
    """

    allowed: bool
    engine: EngineId
    verdict: DecisionVerdictType
    reason: str
    traces: Tuple[AuditTrace, ...]

    def __post_init__(self) -> None:
        """
        Boundary normalization + structural validation.

        Accepts:
        - EngineId / DecisionVerdictType enums
        - canonical string values at construction boundaries

        Internal state is ALWAYS enumâ€‘only.
        """

        # Normalize semantic enums
        try:
            object.__setattr__(self, "engine", EngineId(self.engine))
        except Exception:
            raise ValidationError(
                "engine must be a valid EngineId",
                metadata={"engine": self.engine},
            )

        try:
            object.__setattr__(
                self,
                "verdict",
                DecisionVerdictType(self.verdict),
            )
        except Exception:
            raise ValidationError(
                "verdict must be a valid DecisionVerdictType",
                metadata={"verdict": self.verdict},
            )

        # Structural validation
        if not isinstance(self.allowed, bool):
            raise ValidationError(
                "allowed must be a boolean",
                metadata={"allowed": self.allowed},
            )

        if (self.verdict is DecisionVerdictType.ALLOW) != self.allowed:
            raise ValidationError(
                "allowed must match verdict semantics",
                metadata={
                    "allowed": self.allowed,
                    "verdict": self.verdict.value,
                },
            )

        if not isinstance(self.reason, str) or not self.reason.strip():
            raise ValidationError(
                "reason must be a non-empty string",
                metadata={"reason": self.reason},
            )

        if not isinstance(self.traces, tuple):
            raise ValidationError(
                "traces must be a tuple of AuditTrace",
                metadata={"traces_type": type(self.traces).__name__},
            )

        if any(not isinstance(trace, AuditTrace) for trace in self.traces):
            raise ValidationError(
                "all elements of traces must be AuditTrace instances",
                metadata={
                    "invalid_traces": [
                        type(trace).__name__
                        for trace in self.traces
                        if not isinstance(trace, AuditTrace)
                    ]
                },
            )

    # --------------------------------------------------------
    # Projection helper (explicit, nonâ€‘authoritative)
    # --------------------------------------------------------

    @classmethod
    def from_decision(
        cls,
        decision: Decision,
        *,
        engine: EngineId,
        reason: str,
        traces: Tuple[AuditTrace, ...],
    ) -> "AuditDecision":
        """
        Create an AuditDecision as a projection of a core Decision.

        This helper:
        - DOES NOT change semantics
        - Enforces consistency between Decision and AuditDecision
        """
        return cls(
            allowed=decision.allowed,
            verdict=decision.verdict,
            engine=engine,
            reason=reason,
            traces=traces,
        )


# ============================================================
# Audit Decision ABI (explicit, frozen)
# ============================================================

__all__ = [
    "AuditDecision",
]
