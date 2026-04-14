from dataclasses import dataclass
from typing import Mapping, Any
from core.events import DomainEvent, EventHeaders, EventEnvelope
from core.kernel.invariants import assert_not_none
from control_plane.application.execution.models import ExecutionFrame
from .protocols import FeatureSnapshotSerializer

@dataclass(frozen=True, slots=True)
class SnapshotPublisher:
    """
    Produces a pure EventEnvelope describing the current tenant feature snapshot.
    - No IO: the returned envelope can be persisted by later phases (e.g., outbox).
    - Deterministic: IDs and timestamp sourced from the ExecutionContext (injected).
    """
    topic: str = "features.snapshot"  # logical event type; routing defined later

    def publish(self, frame: ExecutionFrame, serializer: FeatureSnapshotSerializer) -> EventEnvelope:
        assert_not_none(frame, "frame")
        assert_not_none(serializer, "serializer")

        # Prepare canonical event payload (pure, JSON-serializable mapping)
        snapshot_map: Mapping[str, Any] = serializer.to_mapping(frame.feature_snapshot)

        event = DomainEvent(
            event_id=frame.ctx.uuid_provider.new_event_id(),
            event_type=self.topic,
            payload={
                "tenant_id": str(frame.tenant_id),
                "snapshot": dict(snapshot_map),
            },
        )

        headers = EventHeaders(
            correlation_id=frame.correlation_id,
            causation_id=frame.causation_id,
            timestamp_ms=frame.timestamp_ms,
            tenant_id=frame.tenant_id,
        )

        return EventEnvelope.create(event=event, headers=headers)