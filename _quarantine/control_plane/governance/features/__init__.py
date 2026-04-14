"""
AfriHome Control Plane — Governance · Features (Phase 1.4)

Pure, deterministic feature-flag governance:

- FlagRule: immutable targeting rule with deterministic percentage rollout (SHA-256)
- FeatureFlag: immutable definition + deterministic evaluator (deny-wins by priority)
- FeatureStateSnapshot: immutable decision snapshot for audit/replay

No services/adapters/IO here. Application layer orchestrates, passes injected time/ids,
and persists snapshots if needed.
"""
from .flag_rule import FlagRule, ActorKind, RuleEffect
from .feature_flag import FeatureFlag, Target, normalize_feature_key
from .feature_state_snapshot import FeatureStateSnapshot, DecisionSource

__all__ = [
    "ActorKind",
    "RuleEffect",
    "FlagRule",
    "Target",
    "FeatureFlag",
    "normalize_feature_key",
    "DecisionSource",
    "FeatureStateSnapshot",
]