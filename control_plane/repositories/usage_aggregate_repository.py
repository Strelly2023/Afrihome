# control_plane/repositories.usage_aggregate_repository.py
from typing import Optional, Protocol, runtime_checkable

from control_plane.governance.usage.usage_aggregate import UsageAggregate
from control_plane.governance.usage.windowing import UsageGranularity
from core.typing import TenantId, UnixMillis


@runtime_checkable
class UsageAggregateRepository(Protocol):
    """
    Optional repository for precomputed rollups to speed up queries.
    Application layer may compute and save aggregates periodically.
    """

    def get(
        self,
        *,
        tenant_id: TenantId,
        feature_key: str,
        metric_key: str,
        granularity: UsageGranularity,
        start_ms: UnixMillis,
        end_ms: UnixMillis,
    ) -> Optional[UsageAggregate]: ...

    def save(self, agg: UsageAggregate) -> None: ...
