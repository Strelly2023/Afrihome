#control_plane/application/execution/tenant_resolution.py
from typing import Mapping, Optional
from core.typing import TenantId
from core.tenancy import (
    resolve_tenant_context_by_id,
    resolve_tenant_context_by_slug,
    TenantContext,
    TenantResolver,
    validate_tenant_slug,
)
from core.kernel.invariants import assert_not_none
from core.errors import InvariantViolationError
from .constants import HDR_TENANT_ID, HDR_TENANT_SLUG

def resolve_tenant_context(headers: Mapping[str, str], resolver: TenantResolver) -> TenantContext:
    """
    Resolve tenant deterministically using the pure resolver.
    Priority: ID > Slug.
    """
    assert_not_none(headers, "headers")
    assert_not_none(resolver, "resolver")

    tid_raw: Optional[str] = headers.get(HDR_TENANT_ID)
    slug_raw: Optional[str] = headers.get(HDR_TENANT_SLUG)

    if tid_raw and tid_raw.strip():
        return resolve_tenant_context_by_id(resolver, TenantId(tid_raw.strip()))
    if slug_raw and slug_raw.strip():
        s = validate_tenant_slug(slug_raw.strip())
        return resolve_tenant_context_by_slug(resolver, s)

    raise InvariantViolationError("Tenant not provided (x-tenant-id or x-tenant-slug required)")