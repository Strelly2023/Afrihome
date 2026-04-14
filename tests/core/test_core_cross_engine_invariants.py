"""
GA Core — Cross-Engine Invariant Tests
=====================================

Purpose:
- Enforce global safety invariants across decision engines
- Guarantee deny-wins semantics
- Ensure deterministic, order-independent decision normalization

These tests validate SYSTEM LAWS, not engine implementations.

Any failure here indicates a semantic regression in the core.
"""

from afritech.platform.core.decision import (
    combine,
    DecisionVerdict,
)

# ✅ Canonical test helpers (string-only reasons, GA-aligned)
from tests.core.helpers.decision_helpers import allow, deny


# =============================================================
# Invariant 1 — Deny wins globally
# =============================================================

def test_global_deny_wins_over_allows():
    """
    Invariant:
    DENY always dominates ALLOW across all decision engines.
    """
    final = combine(
        [
            allow("rbac", "rbac_allow"),
            allow("policy", "policy_allow"),
            deny("risk", "risk_high"),
            allow("quota", "quota_allow"),
        ]
    )

    assert final.verdict == DecisionVerdict.DENY
    assert "risk_high" in final.reasons


# =============================================================
# Invariant 2 — Soft-deleted tenant blocks all access
# =============================================================

def test_soft_deleted_tenant_blocks_all_access():
    """
    Invariant:
    A soft-deleted tenant results in a system-wide DENY,
    regardless of other authorization signals.
    """
    final = combine(
        [
            allow("rbac"),
            allow("policy"),
            deny("consent", "tenant_soft_deleted"),
            allow("quota"),
        ]
    )

    assert final.verdict == DecisionVerdict.DENY
    assert "tenant_soft_deleted" in final.reasons


# =============================================================
# Invariant 3 — Quota denial overrides authorization
# =============================================================

def test_quota_denial_is_authoritative():
    """
    Invariant:
    Quota denial overrides all authorization ALLOW decisions.
    """
    final = combine(
        [
            allow("rbac"),
            allow("policy"),
            deny("quota", "quota_exceeded"),
        ]
    )

    assert final.verdict == DecisionVerdict.DENY
    assert "quota_exceeded" in final.reasons


# =============================================================
# Invariant 4 — Consent denial is absolute
# =============================================================

def test_consent_denial_is_absolute():
    """
    Invariant:
    Any consent denial results in a final DENY,
    regardless of other engine outcomes.
    """
    final = combine(
        [
            allow("rbac"),
            deny("consent", "consent_revoked"),
            allow("quota"),
        ]
    )

    assert final.verdict == DecisionVerdict.DENY
    assert "consent_revoked" in final.reasons


# =============================================================
# Invariant 5 — Determinism / replay safety
# =============================================================

def test_decision_combination_is_deterministic():
    """
    Invariant:
    Combining the same EngineOutcomes always produces
    the same final Decision.
    """
    outcomes = [
        allow("rbac"),
        deny("risk", "risk_high"),
        allow("quota"),
    ]

    d1 = combine(outcomes)
    d2 = combine(outcomes)

    assert d1 == d2


# =============================================================
# Invariant 6 — Engine order independence
# =============================================================

def test_engine_order_independence():
    """
    Invariant:
    The order in which EngineOutcomes are combined
    must not affect the final Decision.
    """
    d1 = combine(
        [
            allow("rbac"),
            deny("quota", "quota_exceeded"),
            allow("policy"),
        ]
    )

    d2 = combine(
        [
            deny("quota", "quota_exceeded"),
            allow("policy"),
            allow("rbac"),
        ]
    )

    assert d1 == d2


# =============================================================
# Invariant 7 — Multiple denials preserve all reasons
# =============================================================

def test_multiple_denials_preserve_all_reasons():
    """
    Invariant:
    When multiple engines deny, all denial reasons
    must be preserved in the final Decision.
    """
    final = combine(
        [
            deny("quota", "quota_exceeded"),
            deny("risk", "risk_high"),
            deny("consent", "consent_revoked"),
        ]
    )

    assert final.verdict == DecisionVerdict.DENY
    assert set(final.reasons) == {
        "quota_exceeded",
        "risk_high",
        "consent_revoked",
    }