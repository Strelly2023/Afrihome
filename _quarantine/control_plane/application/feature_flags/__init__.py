"""
AfriHome Control Plane — Application/Feature Flags
PHASE: 3.4 (Orchestration only)
IO: NONE | Threads/async: NONE | Deterministic: YES

Exports:
- FeatureDecision, DecisionSource
- FeatureRuleEvaluator, FeatureSnapshotSerializer
- RuleResolver
- FlagReader
- SnapshotPublisher
"""
from .models import FeatureDecision, DecisionSource
from .protocols import FeatureRuleEvaluator, FeatureSnapshotSerializer
from .resolver import RuleResolver
from .reader import FlagReader
from .publisher import SnapshotPublisher

__all__ = [
    "FeatureDecision", "DecisionSource",
    "FeatureRuleEvaluator", "FeatureSnapshotSerializer",
    "RuleResolver",
    "FlagReader",
    "SnapshotPublisher",
]
