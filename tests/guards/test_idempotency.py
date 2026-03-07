
from core.guards import *
from core.typing import UnixMillis


def test_idempotency_flow():
    rec, proceed = idempotency_start(None, key='K', now_ms=UnixMillis(100))
    assert proceed is True and rec.status.name == 'IN_PROGRESS'
    rec2, proceed2 = idempotency_start(rec, key='K', now_ms=UnixMillis(101))
    assert proceed2 is False
    rec3 = idempotency_complete(rec2, response_hash='abc', now_ms=UnixMillis(150))
    assert rec3.status.name == 'COMPLETED'
    assert is_replay_of(rec3, response_hash='abc') is True
