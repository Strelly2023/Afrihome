"""
AfriHome Application — Policy (Orchestration-only)
No IO • Deterministic • Composes RBAC, Feature, Entitlement gates
"""
from .access_decision import AccessDecision, DecisionStage
from .policy_rule import PolicyRule
from .policy_engine import (
    FeatureGate, EntitlementGate, ABACEvaluator,
    PolicyEngine,
)

__all__ = [
    "AccessDecision", "DecisionStage",
    "PolicyRule",
    "FeatureGate", "EntitlementGate", "ABACEvaluator",
    "PolicyEngine",
]