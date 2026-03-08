# control_plane/repositories/provider_repository.py
from __future__ import annotations

from typing import Optional, Protocol, runtime_checkable

from control_plane.governance.integrations.models import ProviderRef
from control_plane.governance.integrations.provider_config import ProviderConfig
from control_plane.governance.tenants.tenant_id import TenantId

# from control_plane.governance.integrations. import ProviderRef   # <-- new


@runtime_checkable
class ProviderRepository(Protocol):
    """
    Protocol boundary for reading provider configs (pure port).
    """

    def get(self, tenant_id: TenantId, ref: ProviderRef) -> Optional[ProviderConfig]:
        """
        Return a ProviderConfig identified by (name, version) within tenant scope, or None.
        """
        ...

    def save(self, tenant_id: TenantId, cfg: ProviderConfig) -> None:
        """
        Idempotent upsert for ProviderConfig.
        """
        ...
