# tests/test_flag_reader.py
from control_plane.application.feature_flags.reader import FlagReader
from control_plane.application.feature_flags.resolver import RuleResolver
from control_plane.application.execution.models import ExecutionFrame, Actor, ActorKind
from core.typing import RoleName, TenantId
from core.execution import ExecutionContext
from core.context import RequestContext
from afritech.platform.control_plane.time.clock import FixedClock
from core.identity.uuid import DeterministicUUIDProvider
from core.typing import RequestId, CorrelationId, CausationId, UnixMillis

class _EchoResolver(RuleResolver):
    # Minimal stub so we can instantiate; relies on real RuleResolver interface
    def __init__(self, evaluator):
        super().__init__(evaluator)

def _frame() -> ExecutionFrame:
    rc = RequestContext(
        request_id=RequestId("r1"),
        correlation_id=CorrelationId("c1"),
        causation_id=CausationId("k1"),
        timestamp_ms=UnixMillis(0),
        tenant_id=TenantId("t1"),
        user_id=None,
    )
    ctx = ExecutionContext(
        request_context=rc,
        clock=FixedClock(UnixMillis(0)),
        uuid_provider=DeterministicUUIDProvider("seed"),
    )
    actor = Actor(kind=ActorKind.SYSTEM, user_id=None, roles=tuple([RoleName("any")]))
    return ExecutionFrame(
        ctx=ctx,
        request_id=rc.request_id,
        correlation_id=rc.correlation_id,
        causation_id=rc.causation_id,
        timestamp_ms=rc.timestamp_ms,
        tenant_id=TenantId("t1"),
        tenant_slug="t1",
        actor=actor,
        feature_snapshot={},
        headers={},
    )

def test_flag_reader_shape(monkeypatch):
    # Monkeypatch a simple evaluator to always enable
    class _Eval:
        def evaluate(self, *, tenant_id, snapshot, actor, key, attributes, now_ms):
            return True, "A", "ok"

    fr = FlagReader(resolver=RuleResolver(evaluator=_Eval()))
    frame = _frame()

    dec = fr.decision(frame, "feature.key")
    assert dec.enabled is True
    assert fr.is_enabled(frame, "feature.key") is True
    assert fr.get_variant(frame, "feature.key", default=None) == "A"