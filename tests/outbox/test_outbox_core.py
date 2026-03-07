
from core.outbox import *
from core.events import DomainEvent, EventHeaders, EventEnvelope
from core.typing import UnixMillis, CorrelationId, CausationId


def _env(eid: str, ts: int):
    ev = DomainEvent(event_id=eid, event_type='user.created', payload={'x': 1})
    hdr = EventHeaders(correlation_id=CorrelationId('c'), causation_id=CausationId('k'), timestamp_ms=UnixMillis(ts))
    return EventEnvelope.create(ev, hdr)


def test_outbox_flow():
    store = InMemoryOutboxStore()
    topic = validate_topic('user.created')
    env = _env('00000000-0000-0000-0000-000000000001', 100)
    write_outbox_record(store, topic, env, UnixMillis(100))
    plan = plan_dispatch(store, topic, UnixMillis(100), limit=10)
    assert len(plan.items) == 1
    eid = plan.items[0].event_id
    apply_success(store, eid)
    plan2 = plan_dispatch(store, topic, UnixMillis(1000), limit=10)
    assert len(plan2.items) == 0
