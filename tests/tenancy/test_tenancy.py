
from core.tenancy import (
    TENANT_SLUG_PATTERN, normalize_tenant_slug, is_valid_tenant_slug, validate_tenant_slug,
    Tenant, TenantContext, DeterministicMapTenantResolver,
    resolve_tenant_context_by_slug, resolve_tenant_context_by_id,
)
from core.typing import TenantId
import pytest


def test_slug_grammar_and_normalization():
    assert normalize_tenant_slug('  ACME  ') == 'acme'
    assert is_valid_tenant_slug('acme')
    assert is_valid_tenant_slug('east-africa-42')
    with pytest.raises(Exception):
        validate_tenant_slug('Bad Slug!')
    assert TENANT_SLUG_PATTERN.match('acme-eu')


def test_tenant_and_context_resolution():
    t1 = Tenant(tenant_id=TenantId('t-1'), slug='Acme', name='Acme Inc')
    t2 = Tenant(tenant_id=TenantId('t-2'), slug='east-africa', name='EA Ops')
    res = DeterministicMapTenantResolver(items=[t1, t2])

    ctx = resolve_tenant_context_by_slug(res, '  acme ')
    assert ctx.slug == 'acme' and ctx.tenant_id == 't-1'

    ctx2 = resolve_tenant_context_by_id(res, TenantId('t-2'))
    assert ctx2.slug == 'east-africa'

    with pytest.raises(Exception):
        resolve_tenant_context_by_slug(res, 'bad slug')
