"""
GA Core â€” Audit Public API Stability Test
----------------------------------------

Purpose:
- Freeze the public ABI of core.audit (L2)
- Prevent accidental symbol exposure
- Enforce explicit API discipline via __all__

RULES:
- The Audit public API is defined ONLY by core/audit/__init__.py __all__
- Any change here is a BREAKING CHANGE and requires an ADR
"""

import afritech.platform.core.audit as audit


def public_api(module):
    """
    Audit ABI is defined strictly by __all__.
    """
    assert hasattr(module, "__all__"), (
        f"{module.__name__} must define __all__"
    )
    return sorted(module.__all__)


def test_core_audit_public_api_stable():
    """
    Audit public API MUST remain stable across GA releases.
    """
    expected = sorted([
        # ----------------------------
        # Core audit artifacts
        # ----------------------------
        "AuditDecision",
        "AuditTrace",
        "AuditExplanation",
        "GovernanceRecord",

        # ----------------------------
        # Composition
        # ----------------------------
        "AuditComposer",

        # ----------------------------
        # Errors (domain-level only)
        # ----------------------------
        "AuditError",
        "InvalidAuditDecisionError",
        "InvalidAuditTraceError",
        "AuditCompositionError",
    ])

    assert public_api(audit) == expected
