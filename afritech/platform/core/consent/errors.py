from __future__ import annotations

"""
GA Enterprise Core â€” Consent Errors
----------------------------------

LAYER: L2 (Pure Engine)
Dependencies: core.errors.base + core.errors.codes + stdlib
Deterministic: YES
Side effects: NONE
IO / Time / Network: NONE

Purpose:
- Define consent-local error hierarchy
- Represent structural or semantic consent failures

Rules:
- MUST derive from CoreError
- MUST use canonical error codes
- MUST be deterministic and replay-safe
- MUST NOT be used to represent allow/deny outcomes
  (legal permission is a *decision*, not an error)
"""

from typing import Optional, Mapping, Any

from afritech.platform.core.errors.base import CoreError
from afritech.platform.core.errors import codes


# ============================================================
# Base Consent Error
# ============================================================

class ConsentError(CoreError):
    """
    Base error for all consent engine failures.

    NOTES:
    - This is an L2 engine error (NOT kernel, NOT L1)
    - Represents structural or semantic misuse of the consent engine
    - NEVER represents a legal allow/deny outcome
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
# Consent Structural / Semantic Errors
# ============================================================

class InvalidConsentDefinitionError(ConsentError):
    """
    Raised when a ConsentDefinition is malformed, incomplete,
    or violates consent grammar or invariants.
    """

    def __init__(
        self,
        *,
        consent_id: str,
        reason: str,
        metadata: Optional[Mapping[str, Any]] = None,
    ) -> None:
        super().__init__(
            message=f"Invalid consent definition for {consent_id!r}: {reason}",
            code=codes.CONSENT_INVALID_DEFINITION,
            metadata={
                "consent_id": consent_id,
                "reason": reason,
                **(dict(metadata) if metadata else {}),
            },
        )


class InvalidConsentSnapshotError(ConsentError):
    """
    Raised when a ConsentSnapshot is malformed,
    inconsistent, or incompatible with a definition.
    """

    def __init__(
        self,
        *,
        consent_id: str,
        reason: str,
        metadata: Optional[Mapping[str, Any]] = None,
    ) -> None:
        super().__init__(
            message=f"Invalid consent snapshot for {consent_id!r}: {reason}",
            code=codes.CONSENT_INVALID_SNAPSHOT,
            metadata={
                "consent_id": consent_id,
                "reason": reason,
                **(dict(metadata) if metadata else {}),
            },
        )


class ConsentEvaluationError(ConsentError):
    """
    Raised when consent evaluation cannot be performed
    due to invalid inputs or structural mismatches.
    """

    def __init__(
        self,
        *,
        consent_id: str,
        reason: str,
        metadata: Optional[Mapping[str, Any]] = None,
    ) -> None:
        super().__init__(
            message=f"Consent evaluation failed for {consent_id!r}: {reason}",
            code=codes.CONSENT_EVALUATION_FAILED,
            metadata={
                "consent_id": consent_id,
                "reason": reason,
                **(dict(metadata) if metadata else {}),
            },
        )


# ============================================================
# Public ABI (explicit, frozen)
# ============================================================

__all__ = [
    "ConsentError",
    "InvalidConsentDefinitionError",
    "InvalidConsentSnapshotError",
    "ConsentEvaluationError",
]
