
import pytest
from core.execution import ExecutionContext, StrictWriteMode, TransactionBoundary
from core.context.request_context import RequestContext
from core.typing import RequestId, CorrelationId, CausationId, UnixMillis
from afritech.platform.control_plane.time.clock import FixedClock
from core.identity.uuid import DeterministicUUIDProvider
from core.errors import InvariantViolationError, StrictWriteViolationError


def _ctx(write: bool = False) -> ExecutionContext:
    req = RequestContext(
        request_id=RequestId('req'),
        correlation_id=CorrelationId('corr'),
        causation_id=CausationId('cause'),
        timestamp_ms=UnixMillis(1),
    )
    return ExecutionContext(
        request_context=req,
        clock=FixedClock(UnixMillis(1)),
        uuid_provider=DeterministicUUIDProvider(seed='s'),
        write_mode=write,
    )


def test_execution_context_methods():
    ctx = _ctx()
    assert ctx.now() == 1
    ctx_w = ctx.with_write_mode()
    assert ctx_w.write_mode is True
    with pytest.raises(InvariantViolationError):
        ctx_w.with_write_mode()


def test_strict_write_enforcement():
    ctx = _ctx()
    with pytest.raises(StrictWriteViolationError):
        StrictWriteMode.require_write(ctx)
    ctx2 = _ctx(write=True)
    StrictWriteMode.require_write(ctx2)


def test_transaction_boundary_enters_write():
    tx = TransactionBoundary(execution_context=_ctx())
    wc = tx.begin()
    assert wc.write_mode is True
