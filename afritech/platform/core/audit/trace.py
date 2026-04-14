from __future__ import annotations

"""
GA Enterprise Core â€” Audit Trace
--------------------------------

LAYER: L2 (Pure Projection Layer)
Dependencies: core.errors.base, core.typing.enums, stdlib only
Deterministic: YES
Side effects: NONE
IO / Time / Network: NONE

Purpose:
- Represent a single factual trace entry explaining
  why an authorization decision occurred
- Project decision evidence for audit and governance

Rules:
- Pure value object
- NO IO, persistence, or identity mapping
- NO kernel dependencies
- NO decision authority
- Structural invariants MUST raise ValidationError
- Enums are the sole semantic authority
"""

from dataclasses import dataclass

from afritech.platform.core.errors.base import ValidationError
from afritech.platform.core.typing.enums import EngineId, Effect


# ============================================================
# Audit Trace (pure projection value object)
# ============================================================

@dataclass(frozen=True, slots=True)
class AuditTrace:
    """
    Single factual audit trace entry.

    Attributes:
        source:
            Originating decision engine (EngineId).
        rule_id:
            Identifier of the rule that participated in the decision.
        effect:
            Effect asserted by the rule (Effect.ALLOW | Effect.DENY).

    NOTES:
    - This is a *projection*, not a decision.
    - It MUST NOT encode precedence or governance logic.
    """

    source: EngineId
    rule_id: str
    effect: Effect

    def __post_init__(self) -> None:
        """
        Boundary normalization + structural validation.

        Accepts:
        - EngineId / Effect enums
        - Canonical string values at construction boundaries

        Internal state is ALWAYS enumâ€‘only.
        """

        # Normalize semantic enums
        try:
            object.__setattr__(self, "source", EngineId(self.source))
        except Exception:
            raise ValidationError(
                "source must be a valid EngineId",
                metadata={"source": self.source},
            )

        try:
            object.__setattr__(self, "effect", Effect(self.effect))
        except Exception:
            raise ValidationError(
                "effect must be a valid Effect",
                metadata={"effect": self.effect},
            )

        # Structural validation
        if not isinstance(self.rule_id, str) or not self.rule_id.strip():
            raise ValidationError(
                "rule_id must be a non-empty string",
                metadata={"rule_id": self.rule_id},
            )


# ============================================================
# Audit Trace ABI (explicit, frozen)
# ============================================================

__all__ = [
    "AuditTrace",
]
