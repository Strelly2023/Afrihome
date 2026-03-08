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

from .models import DecisionSource, FeatureDecision
from .protocols import FeatureRuleEvaluator, FeatureSnapshotSerializer
from .publisher import SnapshotPublisher
from .reader import FlagReader
from .resolver import RuleResolver

__all__ = [
    "FeatureDecision",
    "DecisionSource",
    "FeatureRuleEvaluator",
    "FeatureSnapshotSerializer",
    "RuleResolver",
    "FlagReader",
    "SnapshotPublisher",
]
