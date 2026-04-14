from __future__ import annotations
#afritech/platform/core/consent/grammar.py  
"""
GA Enterprise Core â€” Consent Grammar
-----------------------------------

LAYER: L2 (Pure Engine)
Dependencies: stdlib + core.errors.base
Deterministic: YES
Side effects: NONE
IO / Time / Network: NONE

Purpose:
- Define the canonical grammar for consent states, scopes, and legal bases
- Centralize validation for consent-related inputs
- Ensure deterministic, replay-safe consent semantics

Rules:
- Grammar ONLY (no evaluation, no persistence)
- No kernel imports
- No L1 foundation imports (except CoreError types)
- Uses primitive types exclusively
- Grammar violations MUST raise GrammarViolationError
"""

from typing import Final

from afritech.platform.core.errors.base import GrammarViolationError


# ============================================================
# Consent states
# ============================================================

# State represents the lifecycle of consent.
CONSENT_STATES: Final[set[str]] = {
    "granted",
    "revoked",
    "expired",
}


# ============================================================
# Consent scopes
# ============================================================

# Scope represents *what* the consent applies to.
# These are logical scopes only; mapping to actions
# happens in higher layers.
CONSENT_SCOPES: Final[set[str]] = {
    "data_processing",
    "marketing",
    "analytics",
    "third_party_sharing",
}


# ============================================================
# Legal bases
# ============================================================

# Legal basis represents *why* processing is allowed.
# These align with common regulatory frameworks (e.g. GDPR),
# but remain symbolic and deterministic at L2.
LEGAL_BASES: Final[set[str]] = {
    "consent",
    "contract",
    "legal_obligation",
    "legitimate_interest",
    "vital_interest",
    "public_task",
}


# ============================================================
# Validation helpers (pure)
# ============================================================

def validate_consent_state(state: str) -> str:
    """
    Validate a consent state.

    Returns:
        The normalized state if valid.

    Raises:
        GrammarViolationError if the state is invalid or unsupported.
    """
    if not isinstance(state, str) or not state.strip():
        raise GrammarViolationError(
            "Consent state must be a non-empty string",
            metadata={"state": state},
        )

    value = state.strip()

    if value not in CONSENT_STATES:
        raise GrammarViolationError(
            "Unsupported consent state",
            metadata={
                "state": value,
                "supported": sorted(CONSENT_STATES),
            },
        )

    return value


def validate_consent_scope(scope: str) -> str:
    """
    Validate a consent scope.

    Returns:
        The normalized scope if valid.

    Raises:
        GrammarViolationError if the scope is invalid or unsupported.
    """
    if not isinstance(scope, str) or not scope.strip():
        raise GrammarViolationError(
            "Consent scope must be a non-empty string",
            metadata={"scope": scope},
        )

    value = scope.strip()

    if value not in CONSENT_SCOPES:
        raise GrammarViolationError(
            "Unsupported consent scope",
            metadata={
                "scope": value,
                "supported": sorted(CONSENT_SCOPES),
            },
        )

    return value


def validate_legal_basis(basis: str) -> str:
    """
    Validate a legal basis.

    Returns:
        The normalized legal basis if valid.

    Raises:
        GrammarViolationError if the legal basis is invalid or unsupported.
    """
    if not isinstance(basis, str) or not basis.strip():
        raise GrammarViolationError(
            "Legal basis must be a non-empty string",
            metadata={"basis": basis},
        )

    value = basis.strip()

    if value not in LEGAL_BASES:
        raise GrammarViolationError(
            "Unsupported legal basis",
            metadata={
                "basis": value,
                "supported": sorted(LEGAL_BASES),
            },
        )

    return value


# ============================================================
# Consent Grammar ABI (explicit, frozen)
# ============================================================

__all__ = [
    # Grammar sets
    "CONSENT_STATES",
    "CONSENT_SCOPES",
    "LEGAL_BASES",

    # Validators
    "validate_consent_state",
    "validate_consent_scope",
    "validate_legal_basis",
]
