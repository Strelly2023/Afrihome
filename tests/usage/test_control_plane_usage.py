from core.typing import UnixMillis, TenantId, UserId
from control_plane.governance.features.flag_rule import ActorKind
from control_plane.governance.usage import (
    UsageEvent, UsageGranularity, UsageCounter, usage_aggregate, window_start_ms, window_end_ms,
    aggregate_counters
)

def test_usage_counter_and_aggregate():
    t = TenantId("t-1"); u = UserId("u-1")
    e1 = UsageEvent(feature_key="api.core", metric_key="requests", quantity=2,
                    timestamp_ms=UnixMillis(100_000), tenant_id=t, user_id=u, actor_kind=ActorKind.USER)
    e2 = UsageEvent(feature_key="api.core", metric_key="requests", quantity=3,
                    timestamp_ms=UnixMillis(100_500), tenant_id=t, user_id=u, actor_kind=ActorKind.USER)

    c = UsageCounter.from_event(e1, UsageGranularity.MINUTE)
    c = c.apply(e2)
    assert c.quantity == 5

    # Next minute event → separate counter
    e3 = UsageEvent(feature_key="api.core", metric_key="requests", quantity=4,
                    timestamp_ms=UnixMillis(160_100), tenant_id=t, user_id=u, actor_kind=ActorKind.USER)
    c2 = UsageCounter.from_event(e3, UsageGranularity.MINUTE)

    start = UnixMillis(60_000)   # 00:01 minute
    end   = UnixMillis(180_000)  # 00:03 minute
    agg = aggregate_counters(
        tenant_id=t, feature_key="api.core", metric_key="requests",
        granularity=UsageGranularity.MINUTE, start_ms=start, end_ms=end,
        counters=(c, c2)
    )
    assert agg.total_quantity == 9 and len(agg.windows) == 2