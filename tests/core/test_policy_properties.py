"""
GA Core â€” Policy Property Tests
-------------------------------

Purpose:
- Prove semantic correctness of the Policy engine
- Enforce denyâ€‘wins and defaultâ€‘deny behavior
- Ensure deterministic evaluation

These tests validate PROPERTIES, not implementation steps.
"""

from afritech.platform.core.policy import (
    Condition,
    PolicyRule,
    Policy,
    PolicyEngine,
)


ENGINE = PolicyEngine()


# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------

def eval_policy(
    *,
    rules,
    rbac_allowed=True,
    attributes=None,
):
    if attributes is None:
        attributes = {}
    policy = Policy(tuple(rules))
    return ENGINE.evaluate(
        policy=policy,
        rbac_allowed=rbac_allowed,
        attributes=attributes,
    )


# ------------------------------------------------------------
# Property 1 â€” RBAC false always denies
# ------------------------------------------------------------

def test_rbac_false_always_denies():
    rule = PolicyRule(
        effect="allow",
        conditions=(),
    )

    decision = eval_policy(
        rules=[rule],
        rbac_allowed=False,
        attributes={},
    )

    assert decision.allowed is False
    assert decision.reason.startswith("deny")


# ------------------------------------------------------------
# Property 2 â€” Default deny
# ------------------------------------------------------------

def test_default_deny_when_no_rules_match():
    rule = PolicyRule(
        effect="allow",
        conditions=(
            Condition("region", "eq", "EU"),
        ),
    )

    decision = eval_policy(
        rules=[rule],
        attributes={"region": "US"},
    )

    assert decision.allowed is False
    assert decision.reason == "deny: default"


# ------------------------------------------------------------
# Property 3 â€” Allow rule grants access
# ------------------------------------------------------------

def test_allow_rule_grants_access():
    rule = PolicyRule(
        effect="allow",
        conditions=(
            Condition("env", "eq", "prod"),
        ),
    )

    decision = eval_policy(
        rules=[rule],
        attributes={"env": "prod"},
    )

    assert decision.allowed is True
    assert decision.reason.startswith("allow")


# ------------------------------------------------------------
# Property 4 â€” Deny wins over allow
# ------------------------------------------------------------

def test_deny_wins_over_allow():
    allow = PolicyRule(
        effect="allow",
        conditions=(
            Condition("tier", "eq", "gold"),
        ),
    )

    deny = PolicyRule(
        effect="deny",
        conditions=(
            Condition("region", "eq", "EU"),
        ),
    )

    decision = eval_policy(
        rules=[allow, deny],
        attributes={"tier": "gold", "region": "EU"},
    )

    assert decision.allowed is False
    assert decision.reason.startswith("deny")


# ------------------------------------------------------------
# Property 5 â€” Rule order does not matter
# ------------------------------------------------------------

def test_rule_order_does_not_affect_decision():
    allow = PolicyRule(
        effect="allow",
        conditions=(Condition("env", "eq", "prod"),),
    )
    deny = PolicyRule(
        effect="deny",
        conditions=(Condition("env", "eq", "prod"),),
    )

    d1 = eval_policy(
        rules=[allow, deny],
        attributes={"env": "prod"},
    )

    d2 = eval_policy(
        rules=[deny, allow],
        attributes={"env": "prod"},
    )

    assert d1.allowed is False
    assert d1.allowed == d2.allowed


# ------------------------------------------------------------
# Property 6 â€” Determinism
# ------------------------------------------------------------

def test_policy_determinism():
    rule = PolicyRule(
        effect="allow",
        conditions=(Condition("flag", "exists"),),
    )

    d1 = eval_policy(
        rules=[rule],
        attributes={"flag": True},
    )
    d2 = eval_policy(
        rules=[rule],
        attributes={"flag": True},
    )
    d3 = eval_policy(
        rules=[rule],
        attributes={"flag": True},
    )

    assert d1.allowed is d2.allowed is d3.allowed
    assert d1.reason == d2.reason == d3.reason
