"""
GA Core â€” Tenancy Public API Stability Tests
===========================================

Purpose:
- Freeze the public ABI of core.tenancy (L1)
- Prevent accidental symbol exposure or removal
- Make any API change explicit and ADRâ€‘gated

RULE:
- Tenancy public API is defined ONLY via __all__
- Any change here is a BREAKING CHANGE
"""

import afritech.platform.core.tenancy as tenancy


# =============================================================
# Helper
# =============================================================

def public_api(module):
    """
    Return the explicit GA public API defined via __all__.
    """
    assert hasattr(module, "__all__"), (
        f"{module.__name__} must define __all__"
    )
    return sorted(module.__all__)


# =============================================================
# Tenancy (L1, grammarâ€‘only, GAâ€‘frozen)
# =============================================================

def test_core_tenancy_public_api_stable():
    """
    Tenancy L1 MUST expose a stable, grammarâ€‘only public API.
    """
    expected = sorted([
        # Core models
        "CanonicalTenantId",
        "Tenant",
        "TenantContext",

        # Slug grammar
        "TENANT_SLUG_PATTERN",
        "is_valid_tenant_slug",
        "normalize_tenant_slug",
        "validate_tenant_slug",

        # Tenant ID invariants
        "normalize_tenant_id",
        "validate_tenant_id",
    ])
    assert public_api(tenancy) == expected
