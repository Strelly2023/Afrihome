from core.typing import UnixMillis, TenantId, UserId
from control_plane.governance.features import (
    FeatureFlag, FlagRule, RuleEffect, ActorKind, Target
)

def test_feature_flag_deny_wins_and_percentage():
    flag = FeatureFlag(
        key="beta.dashboard",
        enabled_default=False,
        rules=(
            # Lower priority number ⇒ stronger precedence; DISABLE wins on ties
            FlagRule(rule_id="r1", priority=10, effect=RuleEffect.ENABLE, tenant_slugs=("acme",), percentage=50, salt="s1"),
            FlagRule(rule_id="r2", priority=10, effect=RuleEffect.DISABLE, tenant_slugs=("acme",), percentage=50, salt="s2"),
            FlagRule(rule_id="r3", priority=20, effect=RuleEffect.ENABLE, tenant_slugs=("globex",)),
        )
    )

    target = Target(
        tenant_id=TenantId("t-1"),
        tenant_slug="acme",
        user_id=UserId("u-1"),
        actor_kind=ActorKind.USER,
    )

    snap = flag.evaluate(target=target, now_ms=UnixMillis(1000))
    # Given same priority=10 for r1 and r2, DISABLE wins (deny-wins)
    assert snap.enabled is False
    assert snap.decision_source.name == "RULE"
    assert snap.rule_id in {"r1", "r2"}