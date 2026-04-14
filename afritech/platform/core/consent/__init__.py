"""
GA Enterprise Core â€” Consent Engine
----------------------------------

LAYER: L2 (Pure Engine)
Deterministic: YES
Side effects: NONE

Purpose:
- Expose the frozen public API of the consent engine
- Provide deterministic, replay-safe consent evaluation primitives

Rules:
- Public API is defined ONLY via __all__
- No kernel or foundation dependencies
- No IO, persistence, clocks, or randomness
"""

from afritech.platform.core.consent.grammar import (
    CONSENT_STATES,
    CONSENT_SCOPES,
    LEGAL_BASES,
    validate_consent_state,
    validate_consent_scope,
    validate_legal_basis,
)

from afritech.platform.core.consent.definition import ConsentDefinition
from afritech.platform.core.consent.snapshot import ConsentSnapshot
from afritech.platform.core.consent.decision import ConsentDecision
from afritech.platform.core.consent.evaluation import ConsentEvaluator
from afritech.platform.core.consent.errors import (
    ConsentError,
    InvalidConsentDefinitionError,
    InvalidConsentSnapshotError,
    ConsentEvaluationError,
)

# ============================================================
# Consent Public ABI (Frozen)
# ============================================================

__all__ = [
    # Grammar
    "CONSENT_STATES",
    "CONSENT_SCOPES",
    "LEGAL_BASES",
    "validate_consent_state",
    "validate_consent_scope",
    "validate_legal_basis",

    # Consent models
    "ConsentDefinition",
    "ConsentSnapshot",
    "ConsentDecision",

    # Evaluation engine
    "ConsentEvaluator",

    # Errors
    "ConsentError",
    "InvalidConsentDefinitionError",
    "InvalidConsentSnapshotError",
    "ConsentEvaluationError",
]
