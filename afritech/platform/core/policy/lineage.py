from __future__ import annotations

"""
GA Enterprise Core â€” Policy Lineage
----------------------------------

LAYER: L2 (Pure Engine)
Dependencies: core.policy.version + core.errors.base + stdlib
Deterministic: YES
Side effects: NONE
IO / Time / Network: NONE

Purpose:
- Represent the evolution chain of policy versions
- Enable audit, replay, and diffing in higher layers

Rules:
- Pure value object only
- No kernel dependencies
- No evaluation logic
- Structural invariants MUST raise ValidationError
"""

from dataclasses import dataclass
from typing import Optional

from afritech.platform.core.policy.version import PolicyVersion
from afritech.platform.core.errors.base import ValidationError


# ============================================================
# Policy Lineage Node (pure value object)
# ============================================================

@dataclass(frozen=True, slots=True)
class PolicyLineageNode:
    """
    Represents a single step in policy evolution.

    Attributes:
        version:
            The current policy version.
        parent:
            The immediate predecessor version, if any.
        change_reason:
            Human-readable explanation for the change.
    """

    version: PolicyVersion
    parent: Optional[PolicyVersion]
    change_reason: str

    def __post_init__(self) -> None:
        # ----------------------------------------------------
        # Structural validation (fail-fast, deterministic)
        # ----------------------------------------------------

        if not isinstance(self.version, PolicyVersion):
            raise ValidationError(
                "version must be a PolicyVersion",
                metadata={"version_type": type(self.version).__name__},
            )

        if self.parent is not None and not isinstance(self.parent, PolicyVersion):
            raise ValidationError(
                "parent must be a PolicyVersion or None",
                metadata={
                    "parent_type": type(self.parent).__name__
                },
            )

        if not isinstance(self.change_reason, str) or not self.change_reason.strip():
            raise ValidationError(
                "change_reason must be a non-empty string",
                metadata={"change_reason": self.change_reason},
            )


# ============================================================
# Policy Lineage ABI (explicit, frozen)
# ============================================================

__all__ = [
    "PolicyLineageNode",
]
