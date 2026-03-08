"""
GA Enterprise Core — Tenant Model (Immutable)
---------------------------------------------

LAYER: L3
Dependencies:
- core.typing
- core.tenancy.grammar
- core.kernel.invariants
- core.errors

Rules:
- Immutable
- Deterministic slug normalization
"""

from dataclasses import dataclass
from typing import Optional

from core.kernel.invariants import assert_not_none
from core.tenancy.grammar import validate_tenant_slug
from core.typing import TenantId


@dataclass(frozen=True, slots=True)
class Tenant:
    tenant_id: TenantId
    slug: str
    name: Optional[str] = None

    def __post_init__(self) -> None:
        assert_not_none(self.tenant_id, "tenant_id")
        normalized = validate_tenant_slug(self.slug)
        object.__setattr__(self, "slug", normalized)
