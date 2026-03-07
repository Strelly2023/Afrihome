
from core.guards import CircuitPolicy, CircuitSnapshot, CircuitState, can_execute, record_failure, record_success
from core.typing import UnixMillis


def test_circuit_breaker_flow():
    pol = CircuitPolicy(failure_threshold=2, open_duration_ms=1000, half_open_max_calls=1, half_open_successes_to_close=1)
    snap = CircuitSnapshot()
    # 2 failures -> OPEN
    for t in (10, 11):
        snap, allowed = can_execute(snap, UnixMillis(t), pol)
        assert allowed is True
        snap = record_failure(snap, UnixMillis(t), pol)
    assert snap.state is CircuitState.OPEN
    # Before timeout -> deny
    snap, allowed = can_execute(snap, UnixMillis(1005), pol)
    assert allowed is False
    # After timeout -> HALF_OPEN and allow one probe
    snap, allowed = can_execute(snap, UnixMillis(2010), pol)
    assert snap.state is CircuitState.HALF_OPEN and allowed is True
    # Success closes
    snap = record_success(snap, UnixMillis(2010), pol)
    assert snap.state is CircuitState.CLOSED
