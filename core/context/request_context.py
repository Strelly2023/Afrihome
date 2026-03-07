"""
GA Enterprise Core — Immutable Request Context
----------------------------------------------

LAYER: L1
Dependencies:
- core.typing
- core.kernel.invariants
- core.errors

Rules:
- Fully immutable
- No global state
- No implicit defaults
- All values injected
- No time reads
"""

from dataclasses import dataclass
from typing import Optional

from core.typing import (
    TenantId,
    UserId,
    RequestId,
    CorrelationId,
    CausationId,
    UnixMillis,
)
from core.kernel.invariants import assert_not_none
from core.errors import InvariantViolationError


@dataclass(frozen=True, slots=True)
class RequestContext:
    """
    Immutable request metadata snapshot.
    This object represents a single execution boundary.
    """

    request_id: RequestId
    correlation_id: CorrelationId
    causation_id: CausationId
    timestamp_ms: UnixMillis

    tenant_id: Optional[TenantId] = None
    user_id: Optional[UserId] = None

    def __post_init__(self) -> None:
        assert_not_none(self.request_id, "request_id")
        assert_not_none(self.correlation_id, "correlation_id")
        assert_not_none(self.causation_id, "causation_id")
        assert_not_none(self.timestamp_ms, "timestamp_ms")

        if self.timestamp_ms < 0:
            raise InvariantViolationError("timestamp_ms cannot be negative")

    def is_authenticated(self) -> bool:
        return self.user_id is not None

    def is_multi_tenant(self) -> bool:
        return self.tenant_id is not None

    def to_dict(self) -> dict[str, str | int | None]:
        return {
            "request_id": str(self.request_id),
            "correlation_id": str(self.correlation_id),
            "causation_id": str(self.causation_id),
            "timestamp_ms": int(self.timestamp_ms),
            "tenant_id": str(self.tenant_id) if self.tenant_id is not None else None,
            "user_id": str(self.user_id) if self.user_id is not None else None,
        }