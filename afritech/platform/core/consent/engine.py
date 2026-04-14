from __future__ import annotations

"""
Afritech Core — Consent Decision Engine (GA-SEALED)
--------------------------------------------------

GA-SEALED

Authorization semantics in this file are frozen.
Any semantic change requires an Architecture Decision Record (ADR).

LAYER: L1 (Core)
ROLE: Semantic consent enforcement engine

AUTHORITY:
- This module DEFINES consent semantics.
- Its output is semantic law.
- Downstream layers MUST NOT reinterpret or override its meaning.

CONSTITUTIONAL RULES:
- Pure logic ONLY
- NO IO
- NO time
- NO retries
- NO orchestration
- NO infrastructure or context imports
- MUST be deterministic

SEMANTIC MODEL:
- Missing or revoked consent is a HARD DENY
- Granted consent does NOT grant permission by itself
  (other engines may still deny)
"""

from afritech.platform.core.decision.engine_outcome import EngineOutcome
from afritech.platform.core.typing.enums import EngineId, DecisionVerdictType
from afritech.platform.core.errors import InvariantViolationError


# ---------------------------------------------------------------------
# Public Consent Engine API (L1 Semantic Law)
# ---------------------------------------------------------------------

def evaluate_consent(*, consent_granted: bool) -> EngineOutcome:
    """
    Evaluate consent and return a semantic outcome.

    Args:
        consent_granted:
            True if valid consent has been granted and not revoked.

    Returns:
        EngineOutcome representing consent semantics.

    SEMANTICS:
    - consent_granted == False → DENY
    - consent_granted == True  → ABSTAIN
    """

    if not isinstance(consent_granted, bool):
        raise InvariantViolationError(
            "Consent: consent_granted must be a boolean"
        )

    if consent_granted:
        # Consent satisfied, but does not grant permission by itself.
        # Final authorization depends on other engines (RBAC, Policy, Risk, etc.).
        return _abstain("consent.granted")

    # Consent missing or revoked — absolute semantic deny.
    return _deny("consent.revoked")


# ---------------------------------------------------------------------
# Canonical Outcome Constructors (Semantic Atoms)
# ---------------------------------------------------------------------

def _deny(reason: str) -> EngineOutcome:
    return EngineOutcome(
        engine=EngineId.CONSENT,
        verdict=DecisionVerdictType.DENY,
        reasons=(reason,),
        traces=(),
    )


def _abstain(reason: str) -> EngineOutcome:
    """
    ABSTAIN means:
    - Consent does not block the action
    - Consent does not grant the action
    - Other engines determine the final outcome
    """
    return EngineOutcome(
        engine=EngineId.CONSENT,
        verdict=DecisionVerdictType.ABSTAIN,
        reasons=(reason,),
        traces=(),
    )


# ---------------------------------------------------------------------
# Public ABI (Explicit & Frozen)
# ---------------------------------------------------------------------

__all__ = [
    "evaluate_consent",
]