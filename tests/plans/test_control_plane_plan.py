from core.typing import UnixMillis
from control_plane.governance.plans import (
    Plan, PlanFeature, OveragePolicy, TierMeta, BillingCycle
)

def test_plan_immutable_transitions():
    tier = TierMeta(
        code="pro",
        name="Pro",
        billing_cycle=BillingCycle.MONTHLY,
        currency="USD",
        price_minor=1999,
        description="Professional tier",
        trial_days=14,
        display_order=10,
    )
    pf1 = PlanFeature(feature_key="beta.dashboard", enabled_default=True)
    pf2 = PlanFeature(feature_key="export.csv", enabled_default=True, quota_limit=1000, overage_policy=OveragePolicy.ALLOW_METERED)

    plan = Plan(
        key="core.pro",
        name="Core Pro",
        version=1,
        tier=tier,
        features=(pf1,),
        active=True,
        created_ms=UnixMillis(1000),
        updated_ms=UnixMillis(1000),
    )

    plan2 = plan.with_feature(pf2, UnixMillis(1010))
    assert plan2.get_feature("export.csv").quota_limit == 1000

    plan3 = plan2.without_feature("beta.dashboard", UnixMillis(1020))
    assert plan3.get_feature("beta.dashboard") is None

    plan4 = plan3.bump_version(2, UnixMillis(1030)).rename("Core Pro v2", UnixMillis(1040))
    assert plan4.version == 2
    assert plan4.name == "Core Pro v2"