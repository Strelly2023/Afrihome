"""
GA Core â€” Quota Public API Stability Test
----------------------------------------

Purpose:
- Freeze the public ABI of core.quota (L2)
- Prevent accidental symbol exposure
- Enforce explicit API discipline via __all__

RULES:
- The Quota public API is defined ONLY by core/quota/__init__.py __all__
- Any change here is a BREAKING CHANGE and requires an ADR
"""

import afritech.platform.core.quota as quota


def public_api(module):
    """
    Quota ABI is defined strictly by __all__.
    """
    assert hasattr(module, "__all__"), (
        f"{module.__name__} must define __all__"
    )
    return sorted(module.__all__)


def test_core_quota_public_api_stable():
    """
    Quota public API MUST remain stable across GA releases.
    """
    expected = sorted([
        # ----------------------------
        # Grammar / vocabulary
        # ----------------------------
        "UNITS",
        "SCOPES",
        "DIMENSIONS",
        "validate_unit",
        "validate_scope",
        "validate_dimension",

        # ----------------------------
        # Quota models
        # ----------------------------
        "QuotaDefinition",
        "QuotaSnapshot",
        "QuotaDecision",

        # ----------------------------
        # Evaluation engine
        # ----------------------------
        "QuotaEvaluator",

        # ----------------------------
        # Errors (domain-level only)
        # ----------------------------
        "QuotaError",
        "InvalidQuotaDefinitionError",
        "InvalidQuotaSnapshotError",
        "QuotaEvaluationError",
    ])

    assert public_api(quota) == expected, (
        "Quota public API has changed!\n\n"
        "This is a BREAKING CHANGE.\n"
        "- Update core/quota/__init__.py __all__ intentionally\n"
        "- Add or update an ADR\n"
        "- Then update this test to match\n"
    )
