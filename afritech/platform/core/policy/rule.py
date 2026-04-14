from __future__ import annotations

"""
GA Enterprise Core â€” Policy Rule
--------------------------------

LAYER: L2 (Pure Engine)
Dependencies: core.policy.condition + core.errors.base + stdlib
Deterministic: YES
Side effects: NONE
IO / Time / Network: NONE

Purpose:
- Represent a single policy rule
- Encode allow/deny intent with a set of conditions

Rules:
- Pure value object
- No evaluation logic inside the rule
- No kernel dependencies
- Structural invariants MUST raise ValidationError
"""

from dataclasses import dataclass
from typing import Tuple

from afritech.platform.core.policy.condition import Condition
from afritech.platform.core.errors.base import ValidationError


# ============================================================
# Policy Rule (pure value object)
# ============================================================

@dataclass(frozen=True, slots=True)
class PolicyRule:
    """
    A single policy rule.

    Attributes:
        effect:
            Either 'allow' or 'deny'.
        conditions:
            Tuple of conditions that must all match
            for this rule to apply.
    """

    effect: str               # "allow" or "deny"
    conditions: Tuple[Condition, ...]

    def __post_init__(self) -> None:
        # ----------------------------------------------------
        # Structural validation (fail-fast, deterministic)
        # ----------------------------------------------------

        if self.effect not in {"allow", "deny"}:
            raise ValidationError(
                "effect must be either 'allow' or 'deny'",
                metadata={"effect": self.effect},
            )

        if not isinstance(self.conditions, tuple):
            raise ValidationError(
                "conditions must be a tuple",
                metadata={"conditions_type": type(self.conditions).__name__},
            )

        if any(not isinstance(c, Condition) for c in self.conditions):
            raise ValidationError(
                "all elements of conditions must be Condition instances",
                metadata={
                    "invalid_conditions": [
                        type(c).__name__
                        for c in self.conditions
                        if not isinstance(c, Condition)
                    ]
                },
            )


# ============================================================
# Policy Rule ABI (explicit, frozen)
# ============================================================

__all__ = [
    "PolicyRule",
]
