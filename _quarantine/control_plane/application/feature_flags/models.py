from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Mapping, Optional

class DecisionSource(Enum):
    SNAPSHOT = auto()
    RULE = auto()

@dataclass(frozen=True, slots=True)
class FeatureDecision:
    """
    Immutable decision outcome for a feature key.
    Orchestration-only: this does not perform any storage or side effects.
    """
    key: str
    enabled: bool
    variant: Optional[str]
    reason: str
    source: DecisionSource
    # Inputs for traceability (safe for audit/operator views)
    attributes: Mapping[str, Any]
