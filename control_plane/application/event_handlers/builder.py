# control_plane/application/event_handlers/builder.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Protocol

# DROP EventId from this import:
# from core.events import DomainEvent, EventHeaders, EventEnvelope, EventId
from core.events import DomainEvent, EventEnvelope, EventHeaders  # <- keep these three
from core.kernel.invariants import assert_not_none
from core.typing import CausationId, CorrelationId, TenantId, UnixMillis


class UuidFactory(Protocol):
    """Callable that returns a new event id object (type is intentionally generic for decoupling)."""

    def __call__(self) -> object: ...  # <- was EventId; typing-only change


@dataclass(frozen=True, slots=True)
class EventBuilder:
    """
    Deterministic factory for outbound envelopes.
    Uses injected IDs/time and caller-provided payload. No IO.
    """

    event_type: str

    def __post_init__(self) -> None:
        et = (self.event_type or "").strip()
        if not et:
            raise ValueError("event_type must be a non-empty string")
        object.__setattr__(self, "event_type", et)

    def build(
        self,
        *,
        tenant_id: TenantId,
        correlation_id: CorrelationId,
        causation_id: CausationId,
        timestamp_ms: UnixMillis,
        uuid_new_event_id: UuidFactory,  # () -> object; avoids concrete provider coupling
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
