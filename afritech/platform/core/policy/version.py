from __future__ import annotations

"""
GA Enterprise Core â€” Policy Version
----------------------------------

LAYER: L2 (Pure Engine)
Dependencies: core.errors.base + stdlib
Deterministic: YES
Side effects: NONE
IO / Time / Network: NONE

Purpose:
- Represent an immutable identifier for a specific policy revision
- Support deterministic policy selection by higher layers

Rules:
- Pure value object only
- No kernel dependencies
- No evaluation logic
- Structural invariants MUST raise ValidationError
"""

from dataclasses import dataclass

from afritech.platform.core.errors.base import ValidationError


# ============================================================
# Policy Version (pure value object)
# ============================================================

@dataclass(frozen=True, slots=True)
class PolicyVersion:
    """
    Immutable identifier for a specific policy revision.

    Attributes:
        policy_id:
            Logical policy identifier (e.g. "tenant-governance")
        version:
            Monotonically increasing integer version
        effective_from_ms:
            Unix timestamp in milliseconds at which this version
            becomes effective
    """

    policy_id: str
    version: int
    effective_from_ms: int

    def __post_init__(self) -> None:
        # ----------------------------------------------------
        # Structural validation (fail-fast, deterministic)
        # ----------------------------------------------------

        if not isinstance(self.policy_id, str) or not self.policy_id.strip():
            raise ValidationError(
                "policy_id must be a non-empty string",
                metadata={"policy_id": self.policy_id},
            )

        if not isinstance(self.version, int) or self.version < 0:
            raise ValidationError(
                "version must be a non-negative integer",
                metadata={"version": self.version},
            )

        if not isinstance(self.effective_from_ms, int):
            raise ValidationError(
                "effective_from_ms must be an integer",
                metadata={"effective_from_ms": self.effective_from_ms},
            )
