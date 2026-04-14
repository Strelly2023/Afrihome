from __future__ import annotations

"""
Afritech Core — Risk Decision Engine (GA-SEALED)
------------------------------------------------

GA-SEALED

Authorization semantics in this file are frozen.
Any semantic change requires an Architecture Decision Record (ADR).

LAYER: L1 (Core)
ROLE: Semantic risk evaluation engine

AUTHORITY:
- This module DEFINES risk semantics.
- High or unacceptable risk is an authoritative DENY.
- Acceptable risk NEVER grants access by itself.

CONSTITUTIONAL RULES:
- Pure logic ONLY
- NO IO
- NO time
- NO retries
- NO orchestration
- NO infrastructure or context imports
- MUST be deterministic

SEMANTIC MODEL:
- Unacceptable risk → HARD DENY
- Acceptable / low risk → ABSTAIN
"""

from afritech.platform.core.decision.engine_outcome import EngineOutcome
from afritech.platform.core.typing.enums import EngineId, DecisionVerdictType
from afritech.platform.core.errors import InvariantViolationError


# ---------------------------------------------------------------------
# Public Risk Engine API (L1 Semantic Law)
# ---------------------------------------------------------------------

def evaluate_risk(
    *,
    risk_acceptable: bool,
) -> EngineOutcome:
    """
    Evaluate risk and return a semantic outcome.

    Args:
        risk_acceptable:
            True if assessed risk is within acceptable limits.

    Returns:
        EngineOutcome representing risk semantics.

    SEMANTICS:
    - risk_acceptable == False → DENY
    - risk_acceptable == True  → ABSTAIN
    """

    if not isinstance(risk_acceptable, bool):
        raise InvariantViolationError(
            "Risk: risk_acceptable must be a boolean"
        )

    if risk_acceptable:
        # Risk is acceptable, but this alone never grants permission.
        return _abstain("risk.acceptable")

    # Risk too high — absolute semantic deny.
    return _deny("risk.high")


# ---------------------------------------------------------------------
# Canonical Outcome Constructors (Semantic Atoms)
# ---------------------------------------------------------------------

def _deny(reason: str) -> EngineOutcome:
    """
    DENY means:
    - Risk level is unacceptable
    - Action must not proceed (deny-wins)
    """
    return EngineOutcome(
        engine=EngineId.RISK,
        verdict=DecisionVerdictType.DENY,
        reasons=(reason,),
        traces=(),
    )


def _abstain(reason: str) -> EngineOutcome:
    """
    ABSTAIN means:
    - Risk does not block the action
    - Risk does not grant the action
    - Other engines determine the final outcome
    """
    return EngineOutcome(
        engine=EngineId.RISK,
        verdict=DecisionVerdictType.ABSTAIN,
        reasons=(reason,),
        traces=(),
    )


# ---------------------------------------------------------------------
# Public ABI (Explicit & Frozen)
# ---------------------------------------------------------------------

__all__ = [
    "evaluate_risk",
]