from __future__ import annotations

"""
GA Enterprise Core â€” Audit Errors
--------------------------------

LAYER: L2 (Pure Engine)
Dependencies: core.errors.base + core.errors.codes + stdlib
Deterministic: YES
Side effects: NONE
IO / Time / Network: NONE

Purpose:
- Define audit-local error hierarchy
- Represent structural or semantic audit failures

Rules:
- MUST derive from CoreError
- MUST use canonical error codes
- MUST be deterministic and replay-safe
- MUST NOT be raised for authorization outcomes
  (allow/deny is a *decision*, not an audit error)
"""

from typing import Optional, Mapping, Any

from afritech.platform.core.errors.base import CoreError
from afritech.platform.core.errors import codes


# ============================================================
# Base Audit Error
# ============================================================

class AuditError(CoreError):
    """
    Base error for all audit engine failures.

    NOTES:
    - This is an L2 engine error (NOT kernel, NOT L1)
    - Represents structural or semantic misuse of the audit engine
    - NEVER represents allow/deny authorization outcomes
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
# Audit Structural / Semantic Errors
# ============================================================

class InvalidAuditDecisionError(AuditError):
    """
    Raised when an AuditDecision is malformed or violates invariants.
    """

    def __init__(
        self,
        reason: str,
        *,
        metadata: Optional[Mapping[str, Any]] = None,
    ) -> None:
        super().__init__(
            message=f"Invalid audit decision: {reason}",
            code=codes.AUDIT_INVALID_DECISION,
            metadata={
                "reason": reason,
                **(dict(metadata) if metadata else {}),
            },
        )


class InvalidAuditTraceError(AuditError):
    """
    Raised when an AuditTrace is malformed or inconsistent.
    """

    def __init__(
        self,
        reason: str,
        *,
        metadata: Optional[Mapping[str, Any]] = None,
    ) -> None:
        super().__init__(
            message=f"Invalid audit trace: {reason}",
            code=codes.AUDIT_INVALID_TRACE,
            metadata={
                "reason": reason,
                **(dict(metadata) if metadata else {}),
            },
        )


class AuditCompositionError(AuditError):
    """
    Raised when audit composition fails due to invalid inputs
    or incompatible audit structures.
    """

    def __init__(
        self,
        reason: str,
        *,
        metadata: Optional[Mapping[str, Any]] = None,
    ) -> None:
        super().__init__(
            message=f"Audit composition failed: {reason}",
            code=codes.AUDIT_COMPOSITION_FAILED,
            metadata={
                "reason": reason,
                **(dict(metadata) if metadata else {}),
            },
        )


# ============================================================
# Public ABI (explicit, frozen)
# ============================================================

__all__ = [
    "AuditError",
    "InvalidAuditDecisionError",
    "InvalidAuditTraceError",
    "AuditCompositionError",
]
