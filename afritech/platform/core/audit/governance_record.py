from __future__ import annotations

"""
GA Enterprise Core â€” Audit Governance Record
--------------------------------------------

LAYER: L2 (Pure Engine)
Dependencies: core.errors.base + stdlib
Deterministic: YES
Side effects: NONE
IO / Time / Network: NONE

Purpose:
- Represent declarative governance metadata associated with
  an authorization decision.
- Provide replay-safe, immutable context for compliance and audit.

Rules:
- Pure value object
- No kernel dependencies
- No identity, tenancy, persistence, or IO concerns
- Structural invariants MUST raise ValidationError
"""

from dataclasses import dataclass

from afritech.platform.core.errors.base import ValidationError


# ============================================================
# Governance Record (pure value object)
# ============================================================

@dataclass(frozen=True, slots=True)
class GovernanceRecord:
    """
    Declarative governance metadata for an audit record.

    Attributes:
        policy_id:
            Logical identifier of the policy evaluated
            (e.g. "tenant-governance").
        policy_version:
            Monotonically increasing version number of the policy.
        reason:
            Human-readable explanation for why this governance
            record applies (e.g. "quarterly policy update").
    """

    policy_id: str
    policy_version: int
    reason: str

    def __post_init__(self) -> None:
        # ----------------------------------------------------
        # Structural validation (fail-fast, deterministic)
        # ----------------------------------------------------

        if not isinstance(self.policy_id, str) or not self.policy_id.strip():
            raise ValidationError(
                "policy_id must be a non-empty string",
                metadata={"policy_id": self.policy_id},
            )

        if not isinstance(self.policy_version, int) or self.policy_version < 0:
            raise ValidationError(
                "policy_version must be a non-negative integer",
                metadata={"policy_version": self.policy_version},
            )

        if not isinstance(self.reason, str) or not self.reason.strip():
            raise ValidationError(
                "reason must be a non-empty string",
                metadata={"reason": self.reason},
            )


# ============================================================
# Audit Governance Record ABI (explicit, frozen)
# ============================================================

__all__ = [
    "GovernanceRecord",
]
