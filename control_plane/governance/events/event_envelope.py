# control_plane/governance/events/event_envelope.py
import hashlib
import json
from dataclasses import dataclass
from typing import Optional

from core.events import DomainEvent, EventEnvelope, EventHeaders  # core immutable envelope  # noqa
from core.kernel.invariants import assert_not_none
from core.typing import CausationId, CorrelationId, TenantId, UnixMillis

from .platform_event import PlatformEvent


@dataclass(frozen=True, slots=True)
class PlatformEnvelope:
    """
    Governance-level envelope (pure). Can be converted into core.events.EventEnvelope.
    """

    event: PlatformEvent
    correlation_id: CorrelationId
    causation_id: CausationId
    timestamp_ms: UnixMillis
    tenant_id: Optional[TenantId] = None
    content_hash: Optional[str] = None

    def __post_init__(self) -> None:
        assert_not_none(self.event, "event")
        assert_not_none(self.correlation_id, "correlation_id")
        assert_not_none(self.causation_id, "causation_id")
        assert_not_none(self.timestamp_ms, "timestamp_ms")

    def to_core_envelope(self, *, new_event_id) -> EventEnvelope:
        """
        Convert into a core EventEnvelope using injected ID function (deterministic).
        """
        de = DomainEvent(
            event_id=new_event_id(),
            event_type=self.event.type.name,
            payload=dict(self.event.payload),
        )
        hdr = EventHeaders(
            correlation_id=self.correlation_id,
            causation_id=self.causation_id,
            timestamp_ms=self.timestamp_ms,
            tenant_id=self.tenant_id,
        )
        return EventEnvelope.create(event=de, headers=hdr)

    def compute_hash(self) -> str:
        payload = {
            "type": self.event.type.name,
            "payload": dict(self.event.payload),
            "correlation_id": str(self.correlation_id),
            "causation_id": str(self.causation_id),
            "timestamp_ms": int(self.timestamp_ms),
            "tenant_id": (str(self.tenant_id) if self.tenant_id else None),
        }
        enc = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        return hashlib.sha256(enc).hexdigest()
