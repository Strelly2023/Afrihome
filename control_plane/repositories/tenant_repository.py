from typing import Protocol, Optional, Tuple
from core.typing import TenantId
from typing import Protocol, Optional, runtime_checkable, Iterable
from control_plane.governance.tenants.tenant import Tenant  # adjust path if needed

class TenantRepository(Protocol):
    """
    Pure tenant read contract. No IO in this layer; infra binds it later.
    """
    def get_by_id(self, tenant_id: TenantId) -> Optional[Tenant]: ...
    def get_by_slug(self, slug: str) -> Optional[Tenant]: ...
    def list(self, *, limit: int = 100, offset: int = 0) -> Tuple[Tenant, ...]: ...
    def save(self, tenant: Tenant) -> None: ...
    