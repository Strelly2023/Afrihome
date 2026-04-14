"""
GA Core â€” Risk Public API Stability Test
---------------------------------------

Purpose:
- Freeze the public ABI of core.risk (L2)
- Prevent accidental symbol exposure
- Enforce explicit API discipline via __all__

RULES:
- The Risk public API is defined ONLY by core/risk/__init__.py __all__
- Any change here is a BREAKING CHANGE and requires an ADR
"""

import afritech.platform.core.risk as risk


def public_api(module):
    """
    Risk ABI is defined strictly by __all__.
    """
    assert hasattr(module, "__all__"), (
        f"{module.__name__} must define __all__"
    )
    return sorted(module.__all__)


def test_core_risk_public_api_stable():
    """
    Risk public API MUST remain stable across GA releases.
    """
    expected = sorted([
        # ----------------------------
        # Grammar / vocabulary
        # ----------------------------
        "SIGNALS",
        "SCORE_MIN",
        "SCORE_MAX",
        "BANDS",
        "validate_signal",
        "validate_score",
        "validate_band",

        # ----------------------------
        # Risk models
        # ----------------------------
        "RiskSignal",
        "RiskDefinition",
        "RiskSnapshot",
        "RiskDecision",

        # ----------------------------
        # Evaluation engine
        # ----------------------------
        "RiskEvaluator",

        # ----------------------------
        # Errors (domain-level only)
        # ----------------------------
        "RiskError",
        "InvalidRiskDefinitionError",
        "InvalidRiskSnapshotError",
        "RiskEvaluationError",
    ])

    assert public_api(risk) == expected, (
        "Risk public API has changed!\n\n"
        "This is a BREAKING CHANGE.\n"
        "- Update core/risk/__init__.py __all__ intentionally\n"
        "- Add or update an ADR\n"
        "- Then update this test to match\n"
    )
