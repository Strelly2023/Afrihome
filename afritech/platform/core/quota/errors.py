from __future__ import annotations

"""
GA Enterprise Core â€” Quota Errors
--------------------------------

LAYER: L2 (Pure Engine)
Dependencies: core.errors.base + core.errors.codes + stdlib
Deterministic: YES
Side effects: NONE
IO / Time / Network: NONE

Purpose:
- Define quota-local error hierarchy
- Represent structural or semantic quota failures

Rules:
- MUST derive from CoreError
- MUST use canonical error codes
- MUST be deterministic and replay-safe
- MUST NOT be raised to indicate allow/deny outcomes
  (quota exhaustion is a *decision*, not an error)
"""

from typing import Optional, Mapping, Any

from afritech.platform.core.errors.base import CoreError
from afritech.platform.core.errors import codes


# ============================================================
# Base Quota Error
# ============================================================

class QuotaError(CoreError):
    """
    Base error for all quota engine failures.

    NOTES:
    - This is an L2 engine error (NOT kernel, NOT L1)
    - Represents structural or semantic misuse of the quota engine
    - Never represents quota exhaustion or denial outcomes
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
# Quota Structural / Semantic Errors
# ============================================================

class InvalidQuotaDefinitionError(QuotaError):
    """
    Raised when a quota definition is malformed
    or violates quota grammar or invariants.
    """

    def __init__(
        self,
        *,
        quota_id: str,
        reason: str,
        metadata: Optional[Mapping[str, Any]] = None,
    ) -> None:
        super().__init__(
            message=f"Invalid quota definition for {quota_id!r}: {reason}",
            code=codes.QUOTA_INVALID_DEFINITION,
            metadata={
                "quota_id": quota_id,
                "reason": reason,
                **(dict(metadata) if metadata else {}),
            },
        )


class InvalidQuotaSnapshotError(QuotaError):
    """
    Raised when a quota snapshot is malformed,
    inconsistent, or incompatible with a definition.
    """

    def __init__(
        self,
        *,
        quota_id: str,
        reason: str,
        metadata: Optional[Mapping[str, Any]] = None,
    ) -> None:
        super().__init__(
            message=f"Invalid quota snapshot for {quota_id!r}: {reason}",
            code=codes.QUOTA_INVALID_SNAPSHOT,
            metadata={
                "quota_id": quota_id,
                "reason": reason,
                **(dict(metadata) if metadata else {}),
            },
        )


class QuotaEvaluationError(QuotaError):
    """
    Raised when quota evaluation cannot be performed
    due to invalid inputs or internal structural mismatches.
    """

    def __init__(
        self,
        *,
        quota_id: str,
        reason: str,
        metadata: Optional[Mapping[str, Any]] = None,
    ) -> None:
        super().__init__(
            message=f"Quota evaluation failed for {quota_id!r}: {reason}",
            code=codes.QUOTA_EVALUATION_FAILED,
            metadata={
                "quota_id": quota_id,
                "reason": reason,
                **(dict(metadata) if metadata else {}),
            },
        )


# ============================================================
# Public ABI (explicit, frozen)
# ============================================================

__all__ = [
    "QuotaError",
    "InvalidQuotaDefinitionError",
    "InvalidQuotaSnapshotError",
    "QuotaEvaluationError",
]
