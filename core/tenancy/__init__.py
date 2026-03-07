
"""
GA Enterprise Core — Tenancy Layer (L3)

Purpose:
- SINGLE slug regex authority
- Immutable Tenant & TenantContext
- Pure resolver protocol + deterministic in-memory implementation

Rules:
- No cross-import with RBAC
- No registry/infrastructure
- Deterministic & replay-safe
"""

from .grammar import (
    TENANT_SLUG_PATTERN,
    normalize_tenant_slug,
    is_valid_tenant_slug,
    validate_tenant_slug,
)
from .tenant import Tenant
from .tenant_context import TenantContext
from .resolver import (
    TenantResolver,
    DeterministicMapTenantResolver,
    resolve_tenant_required,
    resolve_tenant_context_by_slug,
    resolve_tenant_context_by_id,
)

__all__ = [
    "TENANT_SLUG_PATTERN",
    "normalize_tenant_slug",
    "is_valid_tenant_slug",
    "validate_tenant_slug",
    "Tenant",
    "TenantContext",
    "TenantResolver",
    "DeterministicMapTenantResolver",
    "resolve_tenant_required",
    "resolve_tenant_context_by_slug",
    "resolve_tenant_context_by_id",
]
