from __future__ import annotations

"""
GA Enterprise Core â€” Tenancy (L1)
--------------------------------

Deterministic, grammar-only tenancy primitives.

Rules:
- No resolution
- No lookup
- No services
"""

# ---------------------------------------------------------------------
# Core tenancy models
# ---------------------------------------------------------------------

from afritech.platform.core.tenancy.tenant import Tenant
from afritech.platform.core.tenancy.tenant_context import TenantContext
from afritech.platform.core.tenancy.tenant_id import CanonicalTenantId

# ---------------------------------------------------------------------
# Grammar (slug)
# ---------------------------------------------------------------------

from afritech.platform.core.tenancy.grammar import (
    TENANT_SLUG_PATTERN,
    normalize_tenant_slug,
    is_valid_tenant_slug,
    validate_tenant_slug,
)

# ---------------------------------------------------------------------
# Invariants (tenant_id)
# ---------------------------------------------------------------------

from afritech.platform.core.tenancy.invariants import (
    normalize_tenant_id,
    validate_tenant_id,   # âœ… CORRECT MODULE
)

# ---------------------------------------------------------------------
# Public GA ABI (explicit, frozen)
# ---------------------------------------------------------------------

__all__ = [
    # Core models
    "Tenant",
    "CanonicalTenantId",
    "TenantContext",

    # Slug grammar
    "TENANT_SLUG_PATTERN",
    "normalize_tenant_slug",
    "is_valid_tenant_slug",
    "validate_tenant_slug",

    # Tenant ID invariants
    "normalize_tenant_id",
    "validate_tenant_id",
]
