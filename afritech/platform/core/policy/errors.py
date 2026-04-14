from __future__ import annotations

"""
GA Enterprise Core â€” Policy Errors
---------------------------------

LAYER: L2 (Pure Engine)
Dependencies: core.errors.base + core.errors.codes + stdlib
Deterministic: YES
Side effects: NONE

Purpose:
- Define policy-local error hierarchy
- Represent malformed, invalid, or un-evaluable policy definitions

Rules:
- MUST derive from CoreError
- MUST use canonical error codes
- MUST be deterministic and replay-safe
- Raised ONLY for structural or semantic policy violations
"""

from typing import Optional, Mapping, Any

from afritech.platform.core.errors.base import CoreError
from afritech.platform.core.errors import codes


# ============================================================
# Base Policy Error
# ============================================================

class PolicyError(CoreError):
    """
    Base error for all policy engine failures.

    NOTES:
    - This is an L2 engine error (NOT kernel, NOT L1)
    - Used exclusively inside core.policy
    """

    def __init__(
        self,
        message: str,
        *,
        code: str,
        metadata: Optional[Mapping[str, Any]] = None,
    ) -> None:
        super().__init__(
            message=message,
            code=code,
            metadata=metadata,
        )


# ============================================================
# Policy Structural / Semantic Errors
# ============================================================

class InvalidPolicyError(PolicyError):
    """
    Raised when a policy definition is malformed, incomplete,
    or violates policy grammar rules.
    """

    def __init__(
        self,
        *,
        policy_id: str,
        reason: str,
        metadata: Optional[Mapping[str, Any]] = None,
    ) -> None:
        super().__init__(
            message=f"Invalid policy definition for {policy_id!r}: {reason}",
            code=codes.POLICY_INVALID_DEFINITION,
            metadata={
                "policy_id": policy_id,
                "reason": reason,
                **(dict(metadata) if metadata else {}),
            },
        )


class PolicyEvaluationError(PolicyError):
    """
    Raised when policy evaluation cannot be completed due to
    structural inconsistencies or invalid inputs.
    """

    def __init__(
        self,
        *,
        policy_id: str,
        reason: str,
        metadata: Optional[Mapping[str, Any]] = None,
    ) -> None:
        super().__init__(
            message=f"Policy evaluation failed for {policy_id!r}: {reason}",
            code=codes.POLICY_EVALUATION_FAILED,
            metadata={
                "policy_id": policy_id,
                "reason": reason,
                **(dict(metadata) if metadata else {}),
            },
        )


# ============================================================
# Public ABI (explicit, frozen)
# ============================================================

__all__ = [
    "PolicyError",
    "InvalidPolicyError",
    "PolicyEvaluationError",
]
