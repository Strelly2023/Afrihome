"""
GA Core â€” Consent Property Tests
-------------------------------

Purpose:
- Prove semantic correctness of the Consent engine
- Enforce fail-safe and deterministic legal evaluation
- Guarantee replay-safe, auditable consent decisions

These tests validate PROPERTIES, not implementations.
"""

from afritech.platform.core.consent import (
    ConsentDefinition,
    ConsentSnapshot,
    ConsentEvaluator,
)

# ============================================================
# Evaluator (pure, stateless)
# ============================================================

EVALUATOR = ConsentEvaluator()


# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------

def eval_consent(
    *,
    definition: ConsentDefinition,
    snapshot: ConsentSnapshot,
    at_ms: int | None = None,
):
    """
    Deterministically evaluate a consent decision.
    """
    return EVALUATOR.evaluate(
        definition=definition,
        snapshot=snapshot,
        at_ms=at_ms,
    )


# ------------------------------------------------------------
# Property 1 â€” Allow when consent is valid
# ------------------------------------------------------------

def test_allow_when_consent_granted_and_valid():
    """
    Consent must be allowed when:
    - scope is covered
    - legal basis is permitted
    - state is 'granted'
    - consent is not expired
    """
    definition = ConsentDefinition(
        consent_id="marketing",
        scopes=("marketing",),
        legal_bases=("consent",),
    )

    snapshot = ConsentSnapshot(
        consent_id="marketing",
        scope="marketing",
        state="granted",
        legal_basis="consent",
        granted_at_ms=1000,
    )

    decision = eval_consent(
        definition=definition,
        snapshot=snapshot,
        at_ms=2000,
    )

    assert decision.allowed is True
    assert decision.state == "granted"
    assert decision.reasons == ("consent_valid",)


# ------------------------------------------------------------
# Property 2 â€” Deny if scope not covered
# ------------------------------------------------------------

def test_deny_when_scope_not_covered():
    """
    Consent must be denied when the requested scope
    is not part of the consent definition.
    """
    definition = ConsentDefinition(
        consent_id="analytics",
        scopes=("analytics",),
        legal_bases=("consent",),
    )

    snapshot = ConsentSnapshot(
        consent_id="analytics",
        scope="marketing",
        state="granted",
        legal_basis="consent",
    )

    decision = eval_consent(
        definition=definition,
        snapshot=snapshot,
    )

    assert decision.allowed is False
    assert "scope_not_covered" in decision.reasons


# ------------------------------------------------------------
# Property 3 â€” Deny if legal basis invalid
# ------------------------------------------------------------

def test_deny_when_legal_basis_invalid():
    """
    Consent must be denied when the legal basis
    is not allowed by the definition.
    """
    definition = ConsentDefinition(
        consent_id="data",
        scopes=("analytics",),
        legal_bases=("consent",),
    )

    snapshot = ConsentSnapshot(
        consent_id="data",
        scope="analytics",
        state="granted",
        legal_basis="contract",
    )

    decision = eval_consent(
        definition=definition,
        snapshot=snapshot,
    )

    assert decision.allowed is False
    assert "invalid_legal_basis" in decision.reasons


# ------------------------------------------------------------
# Property 4 â€” Deny when consent expired
# ------------------------------------------------------------

def test_deny_when_consent_expired():
    """
    Consent must be denied once expiration time is passed.
    """
    definition = ConsentDefinition(
        consent_id="marketing",
        scopes=("marketing",),
        legal_bases=("consent",),
    )

    snapshot = ConsentSnapshot(
        consent_id="marketing",
        scope="marketing",
        state="granted",
        legal_basis="consent",
        granted_at_ms=1000,
        expires_at_ms=2000,
    )

    decision = eval_consent(
        definition=definition,
        snapshot=snapshot,
        at_ms=3000,
    )

    assert decision.allowed is False
    assert decision.state == "expired"
    assert "consent_expired" in decision.reasons


# ------------------------------------------------------------
# Property 5 â€” Fail-safe deny on any non-granted state
# ------------------------------------------------------------

def test_fail_safe_deny_when_not_granted():
    """
    Any state other than 'granted' MUST deny.
    """
    definition = ConsentDefinition(
        consent_id="analytics_service",
        scopes=("analytics",),
        legal_bases=("consent",),
    )

    snapshot = ConsentSnapshot(
        consent_id="analytics_service",
        scope="analytics",
        state="revoked",
        legal_basis="consent",
        revoked_at_ms=1500,
    )

    decision = eval_consent(
        definition=definition,
        snapshot=snapshot,
        at_ms=2000,
    )

    assert decision.allowed is False
    assert decision.state == "revoked"
    assert decision.reasons == ("consent_not_granted",)


# ------------------------------------------------------------
# Property 6 â€” Determinism / replay safety
# ------------------------------------------------------------

def test_consent_determinism():
    """
    Identical inputs must always produce identical outputs.
    """
    definition = ConsentDefinition(
        consent_id="replay",
        scopes=("analytics",),
        legal_bases=("consent",),
    )

    snapshot = ConsentSnapshot(
        consent_id="replay",
        scope="analytics",
        state="granted",
        legal_basis="consent",
        granted_at_ms=1000,
    )

    decisions = [
        eval_consent(
            definition=definition,
            snapshot=snapshot,
            at_ms=2000,
        )
        for _ in range(5)
    ]

    assert all(decision == decisions[0] for decision in decisions)
