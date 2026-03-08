from dataclasses import dataclass
from typing import Iterable, Tuple

from core.typing import TenantId, UnixMillis

from .usage_counter import UsageCounter
from .windowing import UsageGranularity


@dataclass(frozen=True, slots=True)
class UsageAggregate:
    """
    Immutable roll-up of usage over a time range for a given key.
    """

    tenant_id: TenantId
    feature_key: str
    metric_key: str
    granularity: UsageGranularity
    start_ms: UnixMillis
    end_ms: UnixMillis
    total_quantity: int
    windows: Tuple[UsageCounter, ...]  # optional detail for explainability


def aggregate_counters(
    *,
    tenant_id: TenantId,
    feature_key: str,
    metric_key: str,
    granularity: UsageGranularity,
    start_ms: UnixMillis,
    end_ms: UnixMillis,
    counters: Iterable[UsageCounter],
) -> UsageAggregate:
    """
    Pure roll-up over counters in [start_ms, end_ms).
    Assumes `counters` share the same keys/granularity and their windows lie within the range.
    """
    selected = tuple(
        c
        for c in counters
        if c.tenant_id == tenant_id
        and c.feature_key == feature_key
        and c.metric_key == metric_key
        and c.granularity == granularity
        and int(start_ms) <= int(c.window_start_ms) < int(end_ms)
    )
    total = sum(int(c.quantity) for c in selected)
    return UsageAggregate(
        tenant_id=tenant_id,
        feature_key=feature_key,
        metric_key=metric_key,
        granularity=granularity,
        start_ms=start_ms,
        end_ms=end_ms,
        total_quantity=total,
        windows=selected,
    )
