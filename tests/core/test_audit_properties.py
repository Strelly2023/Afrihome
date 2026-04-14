"""
GA Core â€” Audit Property Tests
-----------------------------

Purpose:
- Prove semantic correctness of the Audit engine
- Enforce determinism and replayâ€‘safe behavior
- Validate pure composition of RBAC + Policy decisions

These tests validate PROPERTIES, not implementations.
"""

from afritech.platform.core.audit import (
    AuditTrace,
    AuditComposer,
)


COMPOSER = AuditComposer()


# ------------------------------------------------------------
# Property 1 â€” Determinism
# ------------------------------------------------------------

def test_audit_determinism():
    """
    Same inputs MUST produce identical outputs.
    """
    traces = (
        AuditTrace(source="rbac", rule_id="r1", effect="allow"),
    )

    d1 = COMPOSER.compose(
        rbac_allowed=True,
        policy_allowed=True,
        rbac_traces=traces,
    )

    d2 = COMPOSER.compose(
        rbac_allowed=True,
        policy_allowed=True,
        rbac_traces=traces,
    )

    assert d1 == d2


# ------------------------------------------------------------
# Property 2 â€” Deny wins composition
# ------------------------------------------------------------

def test_audit_deny_wins():
    """
    Any deny MUST result in a deny decision.
    """
    d = COMPOSER.compose(
        rbac_allowed=True,
        policy_allowed=False,
    )

    assert d.allowed is False
    assert d.reason == "deny"


# ------------------------------------------------------------
# Property 3 â€” Allow only if both allow
# ------------------------------------------------------------

def test_audit_allow_only_if_both_allow():
    """
    Allow happens only when both RBAC and Policy allow.
    """
    d = COMPOSER.compose(
        rbac_allowed=True,
        policy_allowed=True,
    )

    assert d.allowed is True
    assert d.reason == "allow"


# ------------------------------------------------------------
# Property 4 â€” Default deny (failâ€‘safe)
# ------------------------------------------------------------

def test_audit_default_deny():
    """
    Missing inputs default safely to deny.
    """
    d = COMPOSER.compose(
        rbac_allowed=False,
        policy_allowed=False,
    )

    assert d.allowed is False
    assert d.reason == "deny"


# ------------------------------------------------------------
# Property 5 â€” Trace preservation
# ------------------------------------------------------------

def test_audit_trace_preservation():
    """
    All provided traces MUST be preserved verbatim.
    """
    rbac_trace = AuditTrace(
        source="rbac",
        rule_id="rbac-rule",
        effect="allow",
    )
    policy_trace = AuditTrace(
        source="policy",
        rule_id="policy-rule",
        effect="deny",
    )

    d = COMPOSER.compose(
        rbac_allowed=True,
        policy_allowed=False,
        rbac_traces=(rbac_trace,),
        policy_traces=(policy_trace,),
    )

    assert d.traces == (rbac_trace, policy_trace)


# ------------------------------------------------------------
# Property 6 â€” Trace order is preserved
# ------------------------------------------------------------

def test_trace_order_preserved():
    """
    Traces MUST retain input order (RBAC before Policy).
    """
    t1 = AuditTrace(source="rbac", rule_id="1", effect="allow")
    t2 = AuditTrace(source="policy", rule_id="2", effect="deny")

    d = COMPOSER.compose(
        rbac_allowed=True,
        policy_allowed=False,
        rbac_traces=(t1,),
        policy_traces=(t2,),
    )

    assert d.traces[0] is t1
    assert d.traces[1] is t2


# ------------------------------------------------------------
# Property 7 â€” No mutation of input traces
# ------------------------------------------------------------

def test_audit_does_not_mutate_inputs():
    """
    Audit composition must not mutate input trace objects.
    """
    rbac_trace = AuditTrace(source="rbac", rule_id="x", effect="allow")
    policy_trace = AuditTrace(source="policy", rule_id="y", effect="deny")

    rbac_traces = (rbac_trace,)
    policy_traces = (policy_trace,)

    _ = COMPOSER.compose(
        rbac_allowed=True,
        policy_allowed=False,
        rbac_traces=rbac_traces,
        policy_traces=policy_traces,
    )

    assert rbac_traces == (rbac_trace,)
    assert policy_traces == (policy_trace,)
