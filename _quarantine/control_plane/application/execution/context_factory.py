#control_plane/application/execution/context_factory.py
"""
AfriHome Control Plane — Application/Execution
PHASE: 3.1 (Orchestration only)
IO: NONE | Threads/async: NONE | Deterministic: YES 
"""
from typing import Mapping, Optional
from core.context import RequestContext
from core.execution import ExecutionContext
from core.identity.uuid import UUIDProvider
from afritech.platform.control_plane.time.clock import Clock
from core.typing import RequestId, CorrelationId, CausationId, UnixMillis
from core.kernel.invariants import assert_not_none
from .constants import (
    HDR_REQUEST_ID, HDR_CORRELATION_ID, HDR_CAUSATION_ID,
)

def _pick(headers: Mapping[str, str], key: str) -> Optional[str]:
    val = headers.get(key)
    return val.strip() if isinstance(val, str) else None

def build_request_context(headers: Mapping[str, str], clock: Clock, uuid: UUIDProvider) -> RequestContext:
    """
    Build a core RequestContext deterministically.
    - If IDs are not provided, mint via the deterministic UUID provider.
    - Timestamp is injected from the provided clock (no direct time reads here).
    """
    assert_not_none(headers, "headers")
    assert_not_none(clock, "clock")
    assert_not_none(uuid, "uuid")

    rid = _pick(headers, HDR_REQUEST_ID) or str(uuid.new_correlation_id())
    cid = _pick(headers, HDR_CORRELATION_ID) or str(uuid.new_correlation_id())
    csn = _pick(headers, HDR_CAUSATION_ID) or str(uuid.new_causation_id())

    now_ms: UnixMillis = clock.now_ms()

    return RequestContext(
        request_id=RequestId(rid),
        correlation_id=CorrelationId(cid),
        causation_id=CausationId(csn),
        timestamp_ms=now_ms,
        tenant_id=None,
        user_id=None,
    )

def new_execution_context(rc: RequestContext, clock: Clock, uuid: UUIDProvider) -> ExecutionContext:
    """
    Wrap the RequestContext into a core ExecutionContext (read-mode).
    """
    assert_not_none(rc, "request_context")
    assert_not_none(clock, "clock")
    assert_not_none(uuid, "uuid")
    return ExecutionContext(request_context=rc, clock=clock, uuid_provider=uuid)