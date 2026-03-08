from dataclasses import dataclass
from typing import Mapping, Any
from core.events import DomainEvent, EventHeaders, EventEnvelope
from core.typing import TenantId, CorrelationId, CausationId, UnixMillis
from core.kernel.invariants import assert_not_none

@dataclass(frozen=True, slots=True)
class EventBuilder:
    """
    Deterministic factory for outbound envelopes.
    Uses injected IDs/time and caller-provided payload. No IO.
    """
    event_type: str

    def build(
        self,
        *,
        tenant_id: TenantId,
        correlation_id: CorrelationId,
        causation_id: CausationId,
        timestamp_ms: UnixMillis,
        uuid_new_event_id,  # function: () -> EventId (kept generic to avoid concrete provider coupling)
        payload: Mapping[str, Any],
    ) -> EventEnvelope:
        assert_not_none(tenant_id, "tenant_id")
        assert_not_none(correlation_id, "correlation_id")
        assert_not_none(causation_id, "causation_id")
        assert_not_none(timestamp_ms, "timestamp_ms")
        assert_not_none(uuid_new_event_id, "uuid_new_event_id")
        assert_not_none(payload, "payload")

        evt = DomainEvent(
            event_id=uuid_new_event_id(),
            event_type=self.event_type,
            payload=dict(payload),
        )
        hdrs = EventHeaders(
            correlation_id=correlation_id,
            causation_id=causation_id,
            timestamp_ms=timestamp_ms,
            tenant_id=tenant_id,
        )
        return EventEnvelope.create(event=evt, headers=hdrs)