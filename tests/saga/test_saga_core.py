
from core.saga import *
from core.typing import AggregateId, UnixMillis, CorrelationId, CausationId


def test_saga_happy_path():
    s = new_saga(
        saga_id=AggregateId('saga-1'),
        steps=('reserve', 'charge', 'ship'),
        started_ms=UnixMillis(100),
        correlation_id=CorrelationId('corr-1'),
        causation_id=CausationId('cause-1'),
    )
    mgr = SagaManager()

    s, _ = mgr.apply(s, StartSaga(), UnixMillis(101))
    s, _ = mgr.apply(s, StepSucceeded('reserve'), UnixMillis(102))
    s, _ = mgr.apply(s, StepSucceeded('charge'), UnixMillis(103))
    s, eff = mgr.apply(s, StepSucceeded('ship'), UnixMillis(104))
    assert s.status.name == 'COMPLETED'
    assert any(ev['type'] == 'saga.completed' for ev in eff.emitted)


def test_saga_failure_and_compensation():
    s = new_saga(
        saga_id=AggregateId('saga-2'),
        steps=('a', 'b'),
        started_ms=UnixMillis(10),
        correlation_id=CorrelationId('c'),
        causation_id=CausationId('k'),
    )
    mgr = SagaManager()
    s, _ = mgr.apply(s, StartSaga(), UnixMillis(11))
    s, _ = mgr.apply(s, StepSucceeded('a'), UnixMillis(12))
    s, _ = mgr.apply(s, StepFailed('b', 'x'), UnixMillis(13))
    assert s.status.name == 'FAILED'
    s, _ = mgr.apply(s, BeginCompensation(), UnixMillis(14))
    s, _ = mgr.apply(s, StepCompensated('a'), UnixMillis(15))
    s, _ = mgr.apply(s, StepCompensated('b'), UnixMillis(16))
    assert s.status.name == 'COMPLETED'
