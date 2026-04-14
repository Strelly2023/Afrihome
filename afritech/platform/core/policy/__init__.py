"""
GA Enterprise Core — Policy Engine
---------------------------------

LAYER: L2 (Pure Engine)
Deterministic: YES
Side effects: NONE

Purpose:
- Expose the frozen public API of the policy engine
- Provide deterministic, conditional authorization primitives

Rules:
- Public API is defined ONLY via __all__
- No kernel or foundation dependencies
- Policy logic is pure and replay-safe
- Decision primitives are sourced ONLY from core.decision (single source of truth)
"""

# ============================================================
# Grammar
# ============================================================

from afritech.platform.core.policy.grammar import (
    OPERATORS,
    validate_operator,
    validate_attribute,
)

# ============================================================
# Core Policy Primitives
# ============================================================

from afritech.platform.core.policy.condition import Condition
from afritech.platform.core.policy.rule import PolicyRule
from afritech.platform.core.policy.policy_definition import Policy

# ============================================================
# Engine (pure evaluation)
# ============================================================

from afritech.platform.core.policy.policy_engine import PolicyEngine

# ============================================================
# Decision (canonical source — DO NOT REDEFINE)
# ============================================================

from afritech.platform.core.decision import Decision

# ============================================================
# Versioning & Lineage
# ============================================================

from afritech.platform.core.policy.version import PolicyVersion
from afritech.platform.core.policy.lineage import PolicyLineageNode
from afritech.platform.core.policy.protocol import PolicyVersionResolver

# ============================================================
# Errors
# ============================================================

from afritech.platform.core.policy.errors import (
    PolicyError,
    InvalidPolicyError,
)

# ============================================================
# Policy Public ABI (Frozen)
# ============================================================

__all__ = [
    # Grammar
    "OPERATORS",
    "validate_operator",
    "validate_attribute",

    # Conditions & rules
    "Condition",
    "PolicyRule",

    # Policy model & evaluation
    "Policy",
    "PolicyEngine",
    "Decision",  # re-exported from core.decision (ABI stability)

    # Versioning & lineage
    "PolicyVersion",
    "PolicyLineageNode",
    "PolicyVersionResolver",

    # Errors
    "PolicyError",
    "InvalidPolicyError",
]