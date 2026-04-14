"""
GA Core â€” Tenancy Property Tests
===============================

Purpose:
- Prove semantic correctness of the Tenancy L1 layer
- Enforce grammar-only, deterministic behavior
- Guarantee replay-safe, side-effect free tenancy primitives

These tests validate PROPERTIES, not implementations.
"""

from afritech.platform.core.tenancy import (
    Tenant,
    TenantContext,
    CanonicalTenantId,
    TENANT_SLUG_PATTERN,
    normalize_tenant_slug,
    is_valid_tenant_slug,
    validate_tenant_slug,
    normalize_tenant_id,
    validate_tenant_id,
)
from afritech.platform.core.errors.base import (
    ValidationError,
    GrammarViolationError,
)


# =============================================================
# Property 1 â€” Tenant slug normalization is deterministic
# =============================================================

def test_tenant_slug_normalization_is_deterministic():
    raw = "  My-Tenant-01  "

    n1 = normalize_tenant_slug(raw)
    n2 = normalize_tenant_slug(raw)
    n3 = normalize_tenant_slug(raw)

    assert n1 == n2 == n3
    assert n1 == "my-tenant-01"


# =============================================================
# Property 2 â€” Tenant slug grammar enforcement
# =============================================================

def test_valid_tenant_slug_is_accepted():
    slug = "tenant-123"

    assert is_valid_tenant_slug(slug) is True
    assert validate_tenant_slug(slug) == slug


def test_invalid_tenant_slug_is_rejected():
    invalid = "Tenant__Bad!!"

    assert is_valid_tenant_slug(invalid) is False

    try:
        validate_tenant_slug(invalid)
    except GrammarViolationError:
        pass
    else:
        assert False, "Expected GrammarViolationError"


# =============================================================
# Property 3 â€” Tenant ID normalization & validation
# =============================================================

def test_tenant_id_normalization_is_deterministic():
    raw = "  TENANT-ABC "

    n1 = normalize_tenant_id(raw)
    n2 = normalize_tenant_id(raw)

    assert n1 == n2
    assert n1 == "tenant-abc"


def test_invalid_tenant_id_is_rejected():
    invalid = "!!bad!!"

    try:
        validate_tenant_id(invalid)
    except GrammarViolationError:
        pass
    else:
        assert False, "Expected GrammarViolationError"


# =============================================================
# Property 4 â€” CanonicalTenantId is a pure value object
# =============================================================

def test_canonical_tenant_id_requires_value():
    try:
        CanonicalTenantId(None)  # type: ignore[arg-type]
    except ValidationError:
        pass
    else:
        assert False, "Expected ValidationError"


def test_canonical_tenant_id_is_stringifiable():
    cid = CanonicalTenantId("tenant-001")

    assert str(cid) == "tenant-001"


# =============================================================
# Property 5 â€” Tenant model enforces grammar deterministically
# =============================================================

def test_tenant_model_normalizes_and_validates_slug():
    tenant = Tenant(
        tenant_id="tenant-123",
        slug="  My-Tenant ",
        name="My Tenant",
    )

    assert tenant.slug == "my-tenant"


def test_tenant_model_rejects_invalid_slug():
    try:
        Tenant(
            tenant_id="tenant-123",
            slug="INVALID!!",
        )
    except GrammarViolationError:
        pass
    else:
        assert False, "Expected GrammarViolationError"


# =============================================================
# Property 6 â€” TenantContext construction
# =============================================================

def test_tenant_context_from_tenant_is_deterministic():
    tenant = Tenant(
        tenant_id="tenant-777",
        slug="tenant-777",
        name="Tenant 777",
    )

    c1 = TenantContext.from_tenant(tenant)
    c2 = TenantContext.from_tenant(tenant)

    assert c1 == c2
    assert c1.tenant_id == tenant.tenant_id
    assert c1.slug == tenant.slug
    assert c1.name == tenant.name


def test_tenant_context_requires_tenant():
    try:
        TenantContext.from_tenant(None)  # type: ignore[arg-type]
    except ValidationError:
        pass
    else:
        assert False, "Expected ValidationError"


# =============================================================
# Property 7 â€” Tenant grammar regex remains authoritative
# =============================================================

def test_tenant_slug_pattern_matches_only_valid_slugs():
    assert TENANT_SLUG_PATTERN.fullmatch("tenant-abc")
    assert TENANT_SLUG_PATTERN.fullmatch("t123")
    assert not TENANT_SLUG_PATTERN.fullmatch("Tenant-ABC")
    assert not TENANT_SLUG_PATTERN.fullmatch("_tenant")
