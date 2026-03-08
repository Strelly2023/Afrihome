from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional

from core.typing import TenantId, UnixMillis, UserId

from .flag_rule import ActorKind


class DecisionSource(Enum):
    RULE = auto()
    DEFAULT = auto()


@dataclass(frozen=True, slots=True)
class FeatureStateSnapshot:
    """
    Immutable snapshot of a single feature decision for a given target.

    Entirely pure; suitable for audit logs or caching at the application layer.
    """

    feature_key: str
    enabled: bool
    decision_source: DecisionSource

    tenant_id: Optional[TenantId]
    tenant_slug: Optional[str]
    user_id: Optional[UserId]
    actor_kind: ActorKind

    timestamp_ms: UnixMillis
    rule_id: Optional[str] = None
    reason: Optional[str] = None
