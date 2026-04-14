from __future__ import annotations

"""
GA Enterprise Core â€” Risk Errors
-------------------------------

LAYER: L2 (Pure Engine)
Dependencies: core.errors.base + core.errors.codes + stdlib
Deterministic: YES
Side effects: NONE
IO / Time / Network: NONE

Purpose:
- Define risk-local error hierarchy
- Represent structural or semantic failures in risk modeling

Rules:
- MUST derive from CoreError
- MUST use canonical error codes
- MUST be deterministic and replay-safe
- MUST NOT be raised to indicate risk outcomes
  (high/critical risk is a *decision*, not an error)
"""

from typing import Optional, Mapping, Any

from afritech.platform.core.errors.base import CoreError
from afritech.platform.core.errors import codes


# ============================================================
# Base Risk Error
# ============================================================

class RiskError(CoreError):
    """
    Base error for all risk engine failures.

    NOTES:
    - This is an L2 engine error (NOT kernel, NOT L1)
    - Represents structural or semantic misuse of the risk engine
    - NEVER represents a high, medium, or critical risk outcome
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
# Risk Structural / Semantic Errors
# ============================================================

class InvalidRiskDefinitionError(RiskError):
    """
    Raised when a RiskDefinition is malformed, incomplete,
    or violates risk grammar or invariants.
    """

    def __init__(
        self,
        *,
        model_id: str,
        reason: str,
        metadata: Optional[Mapping[str, Any]] = None,
    ) -> None:
        super().__init__(
            message=f"Invalid risk definition for {model_id!r}: {reason}",
            code=codes.RISK_INVALID_DEFINITION,
            metadata={
                "model_id": model_id,
                "reason": reason,
                **(dict(metadata) if metadata else {}),
            },
        )


class InvalidRiskSnapshotError(RiskError):
    """
    Raised when a RiskSnapshot is malformed,
    inconsistent, or incompatible with a definition.
    """

    def __init__(
        self,
        *,
        model_id: str,
        reason: str,
        metadata: Optional[Mapping[str, Any]] = None,
    ) -> None:
        super().__init__(
            message=f"Invalid risk snapshot for {model_id!r}: {reason}",
            code=codes.RISK_INVALID_SNAPSHOT,
            metadata={
                "model_id": model_id,
                "reason": reason,
                **(dict(metadata) if metadata else {}),
            },
        )


class RiskEvaluationError(RiskError):
    """
    Raised when risk evaluation cannot be performed
    due to invalid inputs or internal structural mismatches.
    """

    def __init__(
        self,
        *,
        model_id: str,
        reason: str,
        metadata: Optional[Mapping[str, Any]] = None,
    ) -> None:
        super().__init__(
            message=f"Risk evaluation failed for {model_id!r}: {reason}",
            code=codes.RISK_EVALUATION_FAILED,
            metadata={
                "model_id": model_id,
                "reason": reason,
                **(dict(metadata) if metadata else {}),
            },
        )


# ============================================================
# Public ABI (explicit, frozen)
# ============================================================

__all__ = [
    "RiskError",
    "InvalidRiskDefinitionError",
    "InvalidRiskSnapshotError",
    "RiskEvaluationError",
]
