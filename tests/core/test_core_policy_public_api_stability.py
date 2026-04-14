"""
GA Core â€” Policy Public API Stability Test
------------------------------------------

Purpose:
- Freeze the public ABI of core.policy (L2)
- Prevent accidental symbol exposure
- Enforce explicit API discipline via __all__

RULES:
- The Policy public API is defined ONLY by core/policy/__init__.py __all__
- Any change here is a BREAKING CHANGE and requires an ADR
"""

import afritech.platform.core.policy as policy


def public_api(module):
    """
    Policy ABI is defined strictly by __all__.
    """
    assert hasattr(module, "__all__"), (
        f"{module.__name__} must define __all__"
    )
    return sorted(module.__all__)


def test_core_policy_public_api_stable():
    """
    Policy public API MUST remain stable across GA releases.
    """
    expected = sorted([
        # ----------------------------
        # Grammar
        # ----------------------------
        "OPERATORS",
        "validate_operator",
        "validate_attribute",

        # ----------------------------
        # Conditions & rules
        # ----------------------------
        "Condition",
        "PolicyRule",

        # ----------------------------
        # Policy model & evaluation
        # ----------------------------
        "Policy",
        "PolicyEngine",
        "Decision",

        # ----------------------------
        # Versioning & lineage
        # ----------------------------
        "PolicyVersion",
        "PolicyLineageNode",
        "PolicyVersionResolver",

        # ----------------------------
        # Errors (domain-level only)
        # ----------------------------
        "PolicyError",
        "InvalidPolicyError",
    ])

    assert public_api(policy) == expected
