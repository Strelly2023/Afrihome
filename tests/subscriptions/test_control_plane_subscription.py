from core.typing import UnixMillis, TenantId
from control_plane.governance.plans import (
    Plan, PlanFeature, OveragePolicy, TierMeta, BillingCycle
)
from control_plane.governance.subscriptions import (
    Subscription, SubscriptionStatus, PlanChangePolicy,
    build_entitlements_from_plan, apply_entitlement_overrides,
    Entitlement, EntitlementSource
)


def test_entitlements_from_plan_and_override():
    tier = TierMeta(code="pro", name="Pro", billing_cycle=BillingCycle.MONTHLY, currency="USD", price_minor=1999)
    pf_a = PlanFeature(feature_key="export.csv", enabled_default=True, quota_limit=1000, overage_policy=OveragePolicy.ALLOW_METERED)
    pf_b = PlanFeature(feature_key="beta.dashboard", enabled_default=False)

    plan = Plan(
        key="core.pro", name="Core Pro", version=1, tier=tier,
        features=(pf_a, pf_b),
        active=True, created_ms=UnixMillis(1000), updated_ms=UnixMillis(1000)
    )

    base = build_entitlements_from_plan(plan=plan, now_ms=UnixMillis(1200))
    # override: enable beta.dashboard for specific subscription
    override = Entitlement(
        feature_key="beta.dashboard", enabled=True,
        quota_limit=None, overage_policy=OveragePolicy.NONE,
        source=EntitlementSource.OVERRIDE, note="allow beta"
    )
    eff = apply_entitlement_overrides(graph=base, overrides=[override], now_ms=UnixMillis(1210))
    d = {e.feature_key: e for e in eff.items}
    assert d["export.csv"].enabled is True and d["export.csv"].quota_limit == 1000
    assert d["beta.dashboard"].enabled is True and d["beta.dashboard"].source.name == "OVERRIDE"


def test_subscription_lifecycle_and_plan_change():
    sub = Subscription.start(
        tenant_id=TenantId("t-1"),
        plan_key="core.pro",
        plan_version=1,
        started_ms=UnixMillis(1000),
        period_start_ms=UnixMillis(1000),
        period_end_ms=UnixMillis(1600),
        trial_end_ms=UnixMillis(1200),
    )
    assert sub.status is SubscriptionStatus.TRIALING

    # Suspend / Resume
    sub = sub.suspend(UnixMillis(1100)).resume(UnixMillis(1110))
    assert sub.status is SubscriptionStatus.ACTIVE

    # Schedule plan change at next period
    sub = sub.change_plan(new_plan_key="core.enterprise", new_plan_version=2, policy=PlanChangePolicy.NEXT_PERIOD, now_ms=UnixMillis(1500))
    assert sub.next_plan_key == "core.enterprise"
    # Renew -> applies scheduled change
    sub = sub.renew_period(new_start_ms=UnixMillis(1600), new_end_ms=UnixMillis(2200), now_ms=UnixMillis(1600))
    assert sub.plan_key == "core.enterprise" and sub.plan_version == 2

    # Cancel at end of current period
    sub = sub.cancel_at_end(UnixMillis(1610))
    sub = sub.renew_period(new_start_ms=UnixMillis(2200), new_end_ms=UnixMillis(2800), now_ms=UnixMillis(2200))
    assert sub.status is SubscriptionStatus.CANCELED and sub.canceled_at_ms == UnixMillis(2200)