from __future__ import annotations

"""
Afritech Core — RBAC Decision Engine (GA-SEALED)
------------------------------------------------

GA-SEALED

Authorization semantics in this file are frozen.
Any semantic change requires an Architecture Decision Record (ADR).

LAYER: L1 (Core)
ROLE: Semantic role-based access control engine

AUTHORITY:
- This module DEFINES RBAC semantics.
- RBAC answers whether an actor is EVER permitted to attempt an action.
- RBAC does NOT grant final authorization by itself.

CONSTITUTIONAL RULES:
- Pure logic ONLY
- NO IO
- NO time
- NO retries
- NO orchestration
- NO infrastructure or context imports
- MUST be deterministic

SEMANTIC MODEL:
- RBAC failure is an authoritative DENY
- RBAC success is an ALLOW
- Other engines may still deny (policy, consent, quota, risk)
"""

from afritech.platform.core.decision.engine_outcome import EngineOutcome
from afritech.platform.core.typing.enums import EngineId, DecisionVerdictType
from afritech.platform.core.errors import InvariantViolationError


# ---------------------------------------------------------------------
# Public RBAC Engine API (L1 Semantic Law)
# ---------------------------------------------------------------------

def evaluate_rbac(
    *,
    rbac_allowed: bool,
) -> EngineOutcome:
    """
    Evaluate RBAC and return a semantic outcome.

    Args:
        rbac_allowed:
            True if RBAC rules permit the actor to attempt the action.

    Returns:
        EngineOutcome representing RBAC semantics.

    SEMANTICS:
    - rbac_allowed == False → DENY
    - rbac_allowed == True  → ALLOW
    """

    if not isinstance(rbac_allowed, bool):
        raise InvariantViolationError(
            "RBAC: rbac_allowed must be a boolean"
        )

    if rbac_allowed:
        # RBAC permits the action class, but does not finalize authorization.
        return _allow("rbac.allowed")

    # RBAC failure — absolute semantic deny.
    return _deny("rbac.denied")


# ---------------------------------------------------------------------
# Canonical Outcome Constructors (Semantic Atoms)
# ---------------------------------------------------------------------

def _deny(reason: str) -> EngineOutcome:
    """
    DENY means:
    - Actor is NEVER permitted to attempt this action
    - No further evaluation is required (deny-wins)
    """
    return EngineOutcome(
        engine=EngineId.RBAC,
        verdict=DecisionVerdictType.DENY,
        reasons=(reason,),
        traces=(),
    )


def _allow(reason: str) -> EngineOutcome:
    """
    ALLOW means:
    - RBAC permits the attempt
    - Other engines may still deny
    """
    return EngineOutcome(
        engine=EngineId.RBAC,
        verdict=DecisionVerdictType.ALLOW,
        reasons=(reason,),
        traces=(),
    )


# ---------------------------------------------------------------------
# Public ABI (Explicit & Frozen)
# ---------------------------------------------------------------------

__all__ = [
    "evaluate_rbac",
]
