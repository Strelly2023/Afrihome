# tests/helpers/memory_tenant_repo.py
from typing import Optional, Dict

from control_plane.governance.tenants.tenant import Tenant
from control_plane.governance.tenants.tenant_id import TenantId
from control_plane.repositories.tenant_repository import TenantRepository


class MemoryTenantRepository(TenantRepository):
    def __init__(self) -> None:
        self._by_id: Dict[str, Tenant] = {}
        self._by_slug: Dict[str, Tenant] = {}

    def get_by_id(self, tenant_id: TenantId) -> Optional[Tenant]:
        return self._by_id.get(str(tenant_id.value))

    def get_by_slug(self, slug: str) -> Optional[Tenant]:
        return self._by_slug.get(slug)

    def save(self, tenant: Tenant) -> None:
        self._by_id[str(tenant.tenant_id.value)] = tenant
        self._by_slug[tenant.slug] = tenant