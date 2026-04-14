"""
GA Core â€” Consent Public API Stability Test
------------------------------------------

Purpose:
- Freeze the public ABI of core.consent (L2)
- Prevent accidental symbol exposure
- Enforce explicit API discipline via __all__

RULES:
- The Consent public API is defined ONLY by core/consent/__init__.py __all__
- Any change here is a BREAKING CHANGE and requires an ADR
"""

import afritech.platform.core.consent as consent


def public_api(module):
    """
    Consent ABI is defined strictly by __all__.
    """
    assert hasattr(module, "__all__"), (
        f"{module.__name__} must define __all__"
    )
    return sorted(module.__all__)


def test_core_consent_public_api_stable():
    """
    Consent public API MUST remain stable across GA releases.
    """
    expected = sorted([
        # ----------------------------
        # Grammar / vocabulary
        # ----------------------------
        "CONSENT_STATES",
        "CONSENT_SCOPES",
        "LEGAL_BASES",
        "validate_consent_state",
        "validate_consent_scope",
        "validate_legal_basis",

        # ----------------------------
        # Consent models
        # ----------------------------
        "ConsentDefinition",
        "ConsentSnapshot",
        "ConsentDecision",

        # ----------------------------
        # Evaluation engine
        # ----------------------------
        "ConsentEvaluator",

        # ----------------------------
        # Errors (domain-level only)
        # ----------------------------
        "ConsentError",
        "InvalidConsentDefinitionError",
        "InvalidConsentSnapshotError",
        "ConsentEvaluationError",
    ])

    assert public_api(consent) == expected, (
        "Consent public API has changed!\n\n"
        "This is a BREAKING CHANGE.\n"
        "- Update core/consent/__init__.py __all__ intentionally\n"
        "- Add or update an ADR\n"
        "- Then update this test to match\n"
    )
