
from core.context import RequestContext, require_request_id
from core.typing import RequestId, CorrelationId, CausationId, UnixMillis, TenantId, UserId


def test_request_context_immutable_and_derivation():
    base = RequestContext(
        request_id=RequestId('r1'),
        correlation_id=CorrelationId('c1'),
        causation_id=CausationId('k1'),
        timestamp_ms=UnixMillis(10),
    )
    ctx = RequestContext(
        request_id=base.request_id,
        correlation_id=base.correlation_id,
        causation_id=base.causation_id,
        timestamp_ms=base.timestamp_ms,
        tenant_id=TenantId('t-1'),
        user_id=UserId('u-1'),
    )
    assert require_request_id(ctx) == 'r1'
    d = ctx.to_dict()
    assert d['tenant_id'] == 't-1' and d['user_id'] == 'u-1'
