from typing import Any, Mapping, Optional, Protocol, runtime_checkable
from core.typing import TenantId, UnixMillis
from control_plane.application.actors.models import Actor

@runtime_checkable
class FeatureRuleEvaluator(Protocol):
    """
    Pure rule evaluator for feature flags.
    Implementations belong to governance/features (Phase 1) and are bound later.
    This module *only* orchestrates calls to this protocol.
    """
    def evaluate(
        self,
        *,
        tenant_id: TenantId,
        snapshot: Any,            # opaque feature snapshot from 3.1
        actor: Actor,             # application actor surface (3.2)
        key: str,
        attributes: Mapping[str, Any],
        now_ms: UnixMillis,
    ) -> tuple[bool, Optional[str], str]:  # (enabled, variant, reason)
        ...

@runtime_checkable
class FeatureSnapshotSerializer(Protocol):
    """
    Pure serializer for snapshot publishing.
    Implementations provide a stable, JSON-serializable mapping for events.
    """
    def to_mapping(self, snapshot: Any) -> Mapping[str, Any]: ...
