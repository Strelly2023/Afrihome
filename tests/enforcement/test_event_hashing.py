
import pytest
import hashlib

def test_event_envelope_hash_deterministic():
    try:
        from core.events.event import DomainEvent
        from core.events.envelope import EventEnvelope
        from core.events.headers import EventHeaders
        from core.typing import CorrelationId, CausationId, UnixMillis
    except ModuleNotFoundError:
        pytest.skip('events not implemented yet.')
    e1 = DomainEvent(event_id='e1', event_type='user.created', payload={'id': '1', 'name': 'A'})
    e2 = DomainEvent(event_id='e1', event_type='user.created', payload={'id': '1', 'name': 'A'})
    h = EventHeaders(correlation_id=CorrelationId('c'), causation_id=CausationId('k'), timestamp_ms=UnixMillis(1))
    env1 = EventEnvelope.create(e1, h)
    env2 = EventEnvelope.create(e2, h)
    assert env1.content_hash == env2.content_hash
