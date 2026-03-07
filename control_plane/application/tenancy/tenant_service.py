from dataclasses import dataclass
from typing import Optional

from core.execution.execution_context import ExecutionContext
from core.execution.transaction import TransactionBoundary
from core.errors import InvariantViolationError
from core.typing import UnixMillis

from control_plane.governance.tenants.tenant_id import TenantId
from control_plane.governance.tenants.tenant import Tenant
from control_plane.repositories.tenant_repository import TenantRepository


@dataclass(frozen=True, slots=True)
class TenantService:
    """
    Tenancy application service (pure orchestration).

    - No IO or infra here
    - All writes must be within a TransactionBoundary (write_mode)
    - Time and UUIDs are injected from core (ctx.clock / ctx.uuid_provider)
    """
    ctx: ExecutionContext
    repo: TenantRepository

    # ---------- Commands ----------

    def create_tenant(
        self,
        *,
        slug: str,
        data_region: str,
        regulatory_profile: str,
        display_name: str,
    ) -> Tenant:
        # Enter write mode (constitution rule)
        write_ctx = TransactionBoundary(self.ctx).begin()

        now_ms: UnixMillis = write_ctx.now()
        tid = TenantId.new(write_ctx.uuid_provider)

        # Dup check
        if self.repo.get_by_slug(slug) is not None:
            raise InvariantViolationError(f"Tenant slug '{slug}' already exists")

        tenant = Tenant.create(
            tenant_id=tid,
            slug=slug,
            data_region=data_region,
            regulatory_profile=regulatory_profile,
            display_name=display_name,
            now_ms=now_ms,
        )
        self.repo.save(tenant)
        return tenant

    def activate(self, tenant_id: TenantId) -> Tenant:
        write_ctx = TransactionBoundary(self.ctx).begin()
        now_ms: UnixMillis = write_ctx.now()

        t = self._require_tenant(tenant_id).activate(now_ms)
        self.repo.save(t)
        return t

    def suspend(self, tenant_id: TenantId) -> Tenant:
        write_ctx = TransactionBoundary(self.ctx).begin()
        now_ms: UnixMillis = write_ctx.now()

        t = self._require_tenant(tenant_id).suspend(now_ms)
        self.repo.save(t)
        return t

    def rename(self, tenant_id: TenantId, display_name: str) -> Tenant:
        write_ctx = TransactionBoundary(self.ctx).begin()
        now_ms: UnixMillis = write_ctx.now()

        t = self._require_tenant(tenant_id).rename(display_name, now_ms)
        self.repo.save(t)
        return t

    # ---------- Helpers ----------

    def _require_tenant(self, tenant_id: TenantId) -> Tenant:
        t = self.repo.get_by_id(tenant_id)
        if t is None:
            raise InvariantViolationError(f"Tenant not found: {tenant_id}")
        return t