"""
GA Core â€” Public API Stability Tests
===================================

Purpose:
- Enforce explicit, intentional public APIs for GAâ€‘frozen core layers
- Catch accidental additions, removals, or reâ€‘exports
- Make breaking changes explicit and reviewable

RULE:
- Any failure here is a BREAKING CHANGE and must be intentional
  and accompanied by an ADR.
"""

import afritech.platform.core.errors as errors
import afritech.platform.core.typing as typing_mod
import afritech.platform.core.identity as identity
import afritech.platform.core.context as context
import afritech.platform.core.tenancy as tenancy


# =============================================================
# Helper
# =============================================================

def public_api_from_all(module):
    """
    Return the explicit GA public API defined via __all__.
    """
    assert hasattr(module, "__all__"), (
        f"{module.__name__} must define __all__ for GA stability"
    )
    return sorted(module.__all__)


# =============================================================
# Errors (L1, fully frozen)
# =============================================================

def test_errors_api_stable():
    expected = sorted([
        # Kernel / invariant errors
        "CoreError",
        "KernelFrozenError",
        "InvariantViolationError",
        "IdempotencyViolationError",

        # Validation / grammar
        "ValidationError",
        "GrammarViolationError",

        # Authorization / tenancy
        "AuthorizationError",
        "TenantIsolationError",

        # Governance
        "StrictWriteViolationError",
    ])

    assert public_api_from_all(errors) == expected


# =============================================================
# Typing (L1, semiâ€‘open but invariantâ€‘checked)
# =============================================================

def test_typing_api_contains_required_primitives():
    """
    typing is allowed to grow, but core value primitives
    MUST NEVER be removed or renamed.
    """
    api = set(public_api_from_all(typing_mod))

    required = {
        "TenantId",
        "UserId",
        "UnixMillis",
        "RequestId",
        "CorrelationId",
        "CausationId",
        "FrozenModel",
    }

    missing = required - api
    assert not missing, (
        "typing public API is missing required GA primitives: "
        f"{sorted(missing)}"
    )


# =============================================================
# Identity (L1, fully frozen)
# =============================================================

def test_identity_api_stable():
    expected = sorted([
        "User",
        "UserId",
        "IdentityId",
        "IdentityRef",
        "Identity",
        "Principal",
        "IdentityBinding",
        "IdentityProvider",
        "IdentityResolver",
        "IdentityStatus",
        "UUIDProvider",
        "UuidProvider",
        "DeterministicUUIDProvider",
        "validate_email",
        "normalize_display_name",
        "IdentityError",
        "InvalidEmailError",
        "InvalidDisplayNameError",
        "InvalidIdentityTransitionError",
    ])

    assert public_api_from_all(identity) == expected


# =============================================================
# Context (L1, fully frozen)
# =============================================================

def test_context_api_stable():
    expected = sorted([
        "RequestContext",
        "require_tenant_id",
        "require_user_id",
        "require_request_id",
        "require_correlation_id",
    ])

    assert public_api_from_all(context) == expected


# =============================================================
# Tenancy (L1, fully frozen, grammarâ€‘only)
# =============================================================

def test_tenancy_api_stable():
    expected = sorted([
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
    ])

    assert public_api_from_all(tenancy) == expected
