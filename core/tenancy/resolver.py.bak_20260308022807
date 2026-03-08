"""
GA Enterprise Core — Tenant Resolver (Pure)
-------------------------------------------

LAYER: L3
Dependencies:
- core.typing
- core.tenancy.tenant
- core.tenancy.grammar
- core.tenancy.tenant_context
- core.kernel.invariants
- core.errors

Rules:
- No RBAC imports
- No registry/infrastructure
- Deterministic resolution (injected data)
"""

from typing import Dict, Optional, Protocol, runtime_checkable

from core.typing import TenantId
from core.tenancy.tenant import Tenant
from core.tenancy.tenant_context import TenantContext
from core.tenancy.grammar import validate_tenant_slug
from core.kernel.invariants import assert_not_none
from core.errors import InvariantViolationError, GrammarViolationError


@runtime_checkable
class TenantResolver(Protocol):
    def resolve_by_id(self, tenant_id: TenantId) -> Optional[Tenant]: ...
    def resolve_by_slug(self, slug: str) -> Optional[Tenant]: ...


class DeterministicMapTenantResolver:
    """
    Deterministic, in-memory resolver backed by injected data.
    No IO, no background behavior, no cross-module imports.
    """

    def __init__(
        self,
        tenants: Dict[str, Tenant] | None = None,
        *,
        items: Optional[list[Tenant]] = None,
    ) -> None:
        id_index: Dict[str, Tenant] = {}
        slug_index: Dict[str, Tenant] = {}

        def _add(t: Tenant) -> None:
            tid = str(t.tenant_id)
            if tid in id_index:
                raise InvariantViolationError(f"Duplicate tenant_id {tid}")
            s = validate_tenant_slug(t.slug)
            if s in slug_index:
                raise InvariantViolationError(f"Duplicate tenant slug {s}")
            id_index[tid] = t
            slug_index[s] = t

        if tenants is not None:
            for t in tenants.values():
                _add(t)
        if items is not None:
            for t in items:
                _add(t)

        self._by_id: Dict[str, Tenant] = dict(id_index)
        self._by_slug: Dict[str, Tenant] = dict(slug_index)

    def resolve_by_id(self, tenant_id: TenantId) -> Optional[Tenant]:
        return self._by_id.get(str(tenant_id))

    def resolve_by_slug(self, slug: str) -> Optional[Tenant]:
        s = validate_tenant_slug(slug)
        return self._by_slug.get(s)


def resolve_tenant_required(
    resolver: TenantResolver, *, tenant_id: TenantId | None = None, slug: str | None = None
) -> Tenant:
    """
    Resolve a tenant by id or slug. Raises InvariantViolationError if not found.
    """
    assert_not_none(resolver, "resolver")

    if tenant_id is None and slug is None:
        raise InvariantViolationError("Either tenant_id or slug must be provided")

    if tenant_id is not None:
        t = resolver.resolve_by_id(tenant_id)
        if t is None:
            raise InvariantViolationError(f"Tenant not found for id={tenant_id!r}")
        return t

    # slug is not None here
    try:
        s = validate_tenant_slug(slug)  # type: ignore[arg-type]
    except GrammarViolationError as e:
        # Re-raise clearly if normalization/validation fails
        raise e

    t = resolver.resolve_by_slug(s)
    if t is None:
        raise InvariantViolationError(f"Tenant not found for slug={s!r}")
    return t


def resolve_tenant_context_by_slug(resolver: TenantResolver, slug: str) -> TenantContext:
    t = resolve_tenant_required(resolver, slug=slug)
    return TenantContext.from_tenant(t)


def resolve_tenant_context_by_id(resolver: TenantResolver, tenant_id: TenantId) -> TenantContext:
    t = resolve_tenant_required(resolver, tenant_id=tenant_id)
    return TenantContext.from_tenant(t)