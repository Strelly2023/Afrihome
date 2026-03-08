"""
GA Enterprise Core — Tenant Context (Immutable)
-----------------------------------------------

LAYER: L3
Dependencies:
- core.typing
- core.tenancy.tenant
- core.kernel.invariants

Rules:
- Immutable
- No globals/threadlocals
- Deterministic
"""

from dataclasses import dataclass
from typing import Optional

from core.kernel.invariants import assert_not_none
from core.tenancy.tenant import Tenant
from core.typing import TenantId


@dataclass(frozen=True, slots=True)
class TenantContext:
    tenant_id: TenantId
    slug: str
    name: Optional[str] = None

    def __post_init__(self) -> None:
        assert_not_none(self.tenant_id, "tenant_id")
        assert_not_none(self.slug, "slug")

    @staticmethod
    def from_tenant(t: Tenant) -> "TenantContext":
        return TenantContext(tenant_id=t.tenant_id, slug=t.slug, name=t.name)
