
from core.events import DomainEvent, EventHeaders, EventEnvelope
from core.typing import CorrelationId, CausationId, UnixMillis


def test_envelope_hash_stability():
    e = DomainEvent(event_id='e', event_type='t', payload={'a': 1})
    h = EventHeaders(correlation_id=CorrelationId('c'), causation_id=CausationId('k'), timestamp_ms=UnixMillis(1))
    env1 = EventEnvelope.create(e, h)
    env2 = EventEnvelope.create(e, h)
    assert env1.content_hash == env2.content_hash
