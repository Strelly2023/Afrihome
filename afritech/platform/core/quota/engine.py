from __future__ import annotations

"""
Afritech Core — Quota Decision Engine (GA-SEALED)
------------------------------------------------

GA-SEALED

Authorization semantics in this file are frozen.
Any semantic change requires an Architecture Decision Record (ADR).

LAYER: L1 (Core)
ROLE: Semantic quota enforcement engine

AUTHORITY:
- This module DEFINES quota semantics.
- Quota violations are authoritative DENY.
- Quota satisfaction NEVER grants access by itself.

CONSTITUTIONAL RULES:
- Pure logic ONLY
- NO IO
- NO time
- NO retries
- NO orchestration
- NO infrastructure or context imports
- MUST be deterministic

SEMANTIC MODEL:
- Quota exceeded → HARD DENY
- Quota available → ABSTAIN
"""

from afritech.platform.core.decision.engine_outcome import EngineOutcome
from afritech.platform.core.typing.enums import EngineId, DecisionVerdictType
from afritech.platform.core.errors import InvariantViolationError


# ---------------------------------------------------------------------
# Public Quota Engine API (L1 Semantic Law)
# ---------------------------------------------------------------------

def evaluate_quota(
    *,
    quota_available: bool,
) -> EngineOutcome:
    """
    Evaluate quota and return a semantic outcome.

    Args:
        quota_available:
            True if sufficient quota exists for the requested action.

    Returns:
        EngineOutcome representing quota semantics.

    SEMANTICS:
    - quota_available == False → DENY
    - quota_available == True  → ABSTAIN
    """

    if not isinstance(quota_available, bool):
        raise InvariantViolationError(
            "Quota: quota_available must be a boolean"
        )

    if quota_available:
        # Quota satisfied, but quota alone never grants permission.
        return _abstain("quota.available")

    # Quota exceeded — absolute semantic deny.
    return _deny("quota.exceeded")


# ---------------------------------------------------------------------
# Canonical Outcome Constructors (Semantic Atoms)
# ---------------------------------------------------------------------

def _deny(reason: str) -> EngineOutcome:
    return EngineOutcome(
        engine=EngineId.QUOTA,
        verdict=DecisionVerdictType.DENY,
        reasons=(reason,),
        traces=(),
    )


def _abstain(reason: str) -> EngineOutcome:
    """
    ABSTAIN means:
    - Quota does not block the action
    - Quota does not grant the action
    - Other engines determine the final outcome
    """
    return EngineOutcome(
        engine=EngineId.QUOTA,
        verdict=DecisionVerdictType.ABSTAIN,
        reasons=(reason,),
        traces=(),
    )


# ---------------------------------------------------------------------
# Public ABI (Explicit & Frozen)
# ---------------------------------------------------------------------

__all__ = [
    "evaluate_quota",
]