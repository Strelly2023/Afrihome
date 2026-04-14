from __future__ import annotations

"""
GA Enterprise Core â€” Policy Definition
-------------------------------------

LAYER: L2 (Pure Engine)
Dependencies: core.policy.rule + core.errors.base + stdlib
Deterministic: YES
Side effects: NONE
IO / Time / Network: NONE

Purpose:
- Represent an immutable policy definition
- Group policy rules into a single evaluable unit

Rules:
- Pure value object only
- No kernel dependencies
- No evaluation logic
- Structural invariants MUST raise ValidationError
"""

from dataclasses import dataclass
from typing import Tuple

from afritech.platform.core.policy.rule import PolicyRule
from afritech.platform.core.errors.base import ValidationError


# ============================================================
# Policy Definition (pure value object)
# ============================================================

@dataclass(frozen=True, slots=True)
class Policy:
    """
    Immutable policy definition.

    Attributes:
        rules:
            Ordered collection of policy rules.
            Evaluation semantics (denyâ€‘wins, defaultâ€‘deny)
            are applied by PolicyEngine, not here.
    """

    rules: Tuple[PolicyRule, ...]

    def __post_init__(self) -> None:
        # ----------------------------------------------------
        # Structural validation (fail-fast, deterministic)
        # ----------------------------------------------------
        if not isinstance(self.rules, tuple):
            raise ValidationError(
                "rules must be a tuple",
                metadata={"value_type": type(self.rules).__name__},
            )

        if any(not isinstance(rule, PolicyRule) for rule in self.rules):
            raise ValidationError(
                "all elements of rules must be PolicyRule instances",
                metadata={
                    "invalid_rules": [
                        type(r).__name__
                        for r in self.rules
                        if not isinstance(r, PolicyRule)
                    ]
                },
            )


# ============================================================
# Policy Definition ABI (explicit, frozen)
# ============================================================

__all__ = [
    "Policy",
]
