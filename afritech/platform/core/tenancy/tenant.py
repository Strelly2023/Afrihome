from __future__ import annotations

"""
GA Enterprise Core â€” Tenant Model
--------------------------------

LAYER: L1 (Foundation)
Dependencies: core.typing + core.tenancy.grammar + core.errors.base + stdlib
Deterministic: YES
Side effects: NONE

Purpose:
- Represent an immutable tenant value model
- Enforce deterministic tenant slug grammar
- Act as a pure foundation object for higher layers

Rules:
- Immutable
- Grammar enforcement only
- No resolution, lookup, or persistence semantics
- No kernel dependencies
- Structural invariants MUST raise ValidationError
"""

from dataclasses import dataclass
from typing import Optional

from afritech.platform.core.typing import TenantId, FrozenModel
from afritech.platform.core.tenancy.grammar import (
    validate_tenant_slug,
    normalize_tenant_slug,
)
from afritech.platform.core.errors.base import ValidationError


# ============================================================
# Tenant Value Model
# ============================================================

@dataclass(frozen=True, slots=True)
class Tenant(FrozenModel):
    """
    Immutable tenant value model.

    IMPORTANT:
    - This is NOT a registry or resolver handle
    - This object represents WHAT a tenant is, not WHERE it lives
    """

    tenant_id: TenantId
    slug: str
    name: Optional[str] = None

    def __post_init__(self) -> None:
        # ----------------------------------------------------
        # Structural validation
        # ----------------------------------------------------

        if self.tenant_id is None:
            raise ValidationError(
                "tenant_id must not be None",
                metadata={"field": "tenant_id"},
            )

        if not isinstance(self.slug, str):
            raise ValidationError(
                "slug must be a string",
                metadata={"slug": self.slug},
            )

        # ----------------------------------------------------
        # Grammar normalization + validation (authoritative)
        # ----------------------------------------------------

        normalized = normalize_tenant_slug(self.slug)
        validated = validate_tenant_slug(normalized)

        object.__setattr__(self, "slug", validated)
