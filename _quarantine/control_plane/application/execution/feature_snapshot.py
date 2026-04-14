#control_plane/application/execution/feature_snapshot.py

from typing import Protocol, runtime_checkable, Any
from core.typing import TenantId, UnixMillis
from core.kernel.invariants import assert_not_none

@runtime_checkable
class FeatureSnapshotProvider(Protocol):
    """
    Pure provider protocol (no IO here). Infrastructure binds a concrete
    implementation later via repositories/adapters and bootstrap.
    """
    def snapshot_for(self, tenant_id: TenantId, at_ms: UnixMillis) -> Any: ...

def get_feature_snapshot(provider: FeatureSnapshotProvider, tenant_id: TenantId, now_ms: UnixMillis) -> Any:
    assert_not_none(provider, "provider")
    assert_not_none(tenant_id, "tenant_id")
    assert_not_none(now_ms, "now_ms")
    return provider.snapshot_for(tenant_id, now_ms)