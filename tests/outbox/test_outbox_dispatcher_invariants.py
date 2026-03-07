import pytest
from core.outbox.dispatcher import plan_dispatch, apply_success, apply_failure
from core.outbox.memory_store import InMemoryOutboxStore
from core.outbox.model import OutboxRecord, OutboxStatus
from core.events.event import DomainEvent
from core.events.headers import EventHeaders
from core.events.envelope import EventEnvelope
from core.typing import EventId, UnixMillis
from core.errors import InvariantViolationError

def _envelope(eid="evt-1", ts=1234):
    ev = DomainEvent(event_id=EventId(eid), event_type="t", payload={"x": 1})
    hdr = EventHeaders(correlation_id="corr", causation_id="caus", timestamp_ms=UnixMillis(ts))
    return EventEnvelope.create(ev, hdr)

def test_plan_dispatch_limit_must_be_positive():
    store = InMemoryOutboxStore()
    with pytest.raises(InvariantViolationError):
        plan_dispatch(store=store, topic="test.topic", now_ms=UnixMillis(0), limit=0)

def test_apply_success_requires_pending():
    store = InMemoryOutboxStore()
    rec = OutboxRecord(event_id=EventId("e1"), topic="test.topic", envelope=_envelope(), attempts=0, next_attempt_ms=UnixMillis(0), status=OutboxStatus.DISPATCHED)
    store.append(rec)
    with pytest.raises(InvariantViolationError):
        apply_success(store, EventId("e1"))

def test_apply_failure_requires_pending():
    store = InMemoryOutboxStore()
    rec = OutboxRecord(event_id=EventId("e2"), topic="test.topic", envelope=_envelope(), attempts=0, next_attempt_ms=UnixMillis(0), status=OutboxStatus.DISPATCHED)
    store.append(rec)
    with pytest.raises(InvariantViolationError):
        apply_failure(store, EventId("e2"), now_ms=UnixMillis(0))