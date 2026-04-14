from dataclasses import dataclass, replace

from core.typing import UnixMillis
from core.errors import InvariantViolationError
from core.tenancy.grammar import validate_tenant_slug

from .tenant_id import TenantId


@dataclass(frozen=True, slots=True)
class Tenant:
    """
    Immutable Tenant aggregate (pure, deterministic).

    - No I/O, no ORM, no Django
    - Transitions return new instances
    - Timestamps are injected (UnixMillis)
    """
    tenant_id: TenantId
    slug: str
    data_region: str
    regulatory_profile: str
    name: str
    active: bool
    created_ms: UnixMillis
    updated_ms: UnixMillis

    def __post_init__(self) -> None:
        # Single canonical slug authority (core.tenancy.grammar)
        _ = validate_tenant_slug(self.slug)

        if not isinstance(self.name, str) or not self.name.strip():
            raise InvariantViolationError("Tenant.display_name cannot be empty")

        if int(self.created_ms) < 0 or int(self.updated_ms) < 0:
            raise InvariantViolationError("Timestamps must be non-negative")

        if int(self.updated_ms) < int(self.created_ms):
            raise InvariantViolationError("updated_ms cannot be earlier than created_ms")

    # ---------- Pure transitions ----------

    def ensure_active(self) -> "Tenant":
        if not self.active:
            raise InvariantViolationError("Tenant is not active")
        return self

    def activate(self, now_ms: UnixMillis) -> "Tenant":
        return replace(self, active=True, updated_ms=now_ms)

    def suspend(self, now_ms: UnixMillis) -> "Tenant":
        return replace(self, active=False, updated_ms=now_ms)

    def rename(self, display_name: str, now_ms: UnixMillis) -> "Tenant":
        d = (display_name or "").strip()
        if not d:
            raise InvariantViolationError("Display name cannot be empty")
        return replace(self, name=d, updated_ms=now_ms)

    # ---------- Pure constructor ----------

    @staticmethod
    def create(
        *,
        tenant_id: TenantId,
        slug: str,
        data_region: str,
        regulatory_profile: str,
        display_name: str,
        now_ms: UnixMillis,
    ) -> "Tenant":
        # Validate slug via canonical authority
        s = validate_tenant_slug(slug)
        d = (display_name or "").strip()
        if not d:
            raise InvariantViolationError("Display name cannot be empty")

        return Tenant(
            tenant_id=tenant_id,
            slug=s,
            data_region=data_region,
            regulatory_profile=regulatory_profile,
            name=d,
            active=True,
            created_ms=now_ms,
            updated_ms=now_ms,
        )