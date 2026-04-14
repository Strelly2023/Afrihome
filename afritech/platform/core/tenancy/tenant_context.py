from __future__ import annotations

"""
GA Enterprise Core â€” Tenant Context
----------------------------------

LAYER: L1 (Foundation)
Dependencies: core.typing + core.tenancy.tenant + core.errors.base + stdlib
Deterministic: YES
Side effects: NONE

Purpose:
- Carry immutable, tenant-scoped metadata
- Bridge Tenant value models into request/context flows

Rules:
- Immutable
- No globals or threadlocals
- No authorization or resolution logic
- No kernel dependencies
- Structural invariants MUST raise ValidationError
"""

from dataclasses import dataclass
from typing import Optional

from afritech.platform.core.typing import (
    TenantId,
    FrozenModel,
)
from afritech.platform.core.tenancy.tenant import Tenant
from afritech.platform.core.errors.base import ValidationError


# ============================================================
# Tenant Context
# ============================================================

@dataclass(frozen=True, slots=True)
class TenantContext(FrozenModel):
    """
    Immutable tenant-scoped context snapshot.

    This object is typically embedded into higher-level
    request or execution contexts to provide deterministic
    tenant metadata.

    IMPORTANT:
    - This is NOT a tenant resolver
    - This carries metadata only
    """

    tenant_id: TenantId
    slug: str
    name: Optional[str] = None

    def __post_init__(self) -> None:
        # ----------------------------------------------------
        # Structural validation (fail-fast, deterministic)
        # ----------------------------------------------------

        if self.tenant_id is None:
            raise ValidationError(
                "tenant_context.tenant_id must not be None",
                metadata={"field": "tenant_id"},
            )

        if not isinstance(self.slug, str) or not self.slug.strip():
            raise ValidationError(
                "tenant_context.slug must be a non-empty string",
                metadata={"slug": self.slug},
            )

    # --------------------------------------------------------
    # Factory
    # --------------------------------------------------------

    @staticmethod
    def from_tenant(tenant: Tenant) -> "TenantContext":
        """
        Create a TenantContext from a Tenant value model.
        """
        if tenant is None:
            raise ValidationError(
                "tenant must not be None",
                metadata={"argument": "tenant"},
            )

        return TenantContext(
            tenant_id=tenant.tenant_id,
            slug=tenant.slug,
            name=tenant.name,
        )


# ============================================================
# Tenant Context ABI (explicit, frozen)
# ============================================================

__all__ = [
    "TenantContext",
]
