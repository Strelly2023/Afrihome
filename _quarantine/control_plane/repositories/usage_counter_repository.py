#control_plane/repositories.usage_counter_repository.py
from typing import Protocol, Iterable, runtime_checkable

from control_plane.governance.usage.usage_counter import UsageCounter
from control_plane.governance.usage.windowing import UsageGranularity
from core.typing import TenantId, UnixMillis



@runtime_checkable
class UsageCounterRepository(Protocol):
    """
    Persist per-window counters (e.g., MINUTE/HOUR/DAY) for {tenant, feature, metric}.

    Typical operations
    ------------------
    - upsert_window(counter)
    - list_windows(range) for aggregation & enforcement
    """

    def upsert(self, counter: UsageCounter) -> None: ...

    def list_windows(
        self,
        *,
        tenant_id: TenantId,
        feature_key: str,
        metric_key: str,
        granularity: UsageGranularity,
        start_ms: UnixMillis,
        end_ms: UnixMillis,
    ) -> Iterable[UsageCounter]: ...