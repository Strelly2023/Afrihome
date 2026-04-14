from __future__ import annotations

"""
GA Enterprise Core â€” Quota Decision
----------------------------------

LAYER: L2 (Pure Engine)
Dependencies: core.errors.base + stdlib
Deterministic: YES
Side effects: NONE
IO / Time / Network: NONE

Purpose:
- Represent the outcome of quota evaluation
- Provide a deterministic, replay-safe allow/deny decision

Rules:
- Pure value object
- No kernel dependencies
- No persistence, mutation, or side effects
- Structural invariants MUST raise ValidationError
"""

from dataclasses import dataclass
from typing import Optional

from afritech.platform.core.errors.base import ValidationError


# ============================================================
# Quota Decision (pure value object)
# ============================================================

@dataclass(frozen=True, slots=True)
class QuotaDecision:
    """
    Result of quota evaluation.

    Attributes:
        allowed:
            Whether the action is permitted under the quota.
        reason:
            Machine-readable reason for the decision
            (e.g. "allow", "deny:limit_exceeded").
        limit:
            The quota limit that was evaluated.
        used:
            The amount of usage consumed so far.
        remaining:
            Remaining allowance after evaluation, if applicable.
    """

    allowed: bool
    reason: str
    limit: int
    used: int
    remaining: Optional[int] = None

    def __post_init__(self) -> None:
        # ----------------------------------------------------
        # Structural validation (fail-fast, deterministic)
        # ----------------------------------------------------

        if not isinstance(self.allowed, bool):
            raise ValidationError(
                "allowed must be a boolean",
                metadata={"allowed": self.allowed},
            )

        if not isinstance(self.reason, str) or not self.reason.strip():
            raise ValidationError(
                "reason must be a non-empty string",
                metadata={"reason": self.reason},
            )

        if not isinstance(self.limit, int) or self.limit < 0:
            raise ValidationError(
                "limit must be a non-negative integer",
                metadata={"limit": self.limit},
            )

        if not isinstance(self.used, int) or self.used < 0:
            raise ValidationError(
                "used must be a non-negative integer",
                metadata={"used": self.used},
            )

        if self.remaining is not None:
            if not isinstance(self.remaining, int) or self.remaining < 0:
                raise ValidationError(
                    "remaining must be None or a non-negative integer",
                    metadata={"remaining": self.remaining},
                )

        # ----------------------------------------------------
        # Consistency invariants
        # ----------------------------------------------------

        if self.remaining is not None:
            expected = max(self.limit - self.used, 0)
            if self.remaining != expected:
                raise ValidationError(
                    "remaining must equal max(limit - used, 0)",
                    metadata={
                        "limit": self.limit,
                        "used": self.used,
                        "remaining": self.remaining,
                        "expected": expected,
                    },
                )


# ============================================================
# Quota Decision ABI (explicit, frozen)
# ============================================================

__all__ = [
    "QuotaDecision",
]
