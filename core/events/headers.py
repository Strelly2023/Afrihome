"""
GA Enterprise Core — Event Headers
----------------------------------

LAYER: L2
Dependencies:
- core.typing
- core.kernel.invariants

Rules:
- Immutable
- Canonical fields only
"""

from dataclasses import dataclass

from core.typing import (
    CorrelationId,
    CausationId,
    TenantId,
    UnixMillis,
)
from core.kernel.invariants import assert_not_none
from core.errors import InvariantViolationError


@dataclass(frozen=True, slots=True)
class EventHeaders:
    """
    Canonical event headers.
    """

    correlation_id: CorrelationId
    causation_id: CausationId
    timestamp_ms: UnixMillis
    tenant_id: TenantId | None = None

    def __post_init__(self) -> None:
        assert_not_none(self.correlation_id, "correlation_id")
        assert_not_none(self.causation_id, "causation_id")
        assert_not_none(self.timestamp_ms, "timestamp_ms")

        if self.timestamp_ms < 0:
            raise InvariantViolationError("timestamp_ms cannot be negative")

    def to_dict(self) -> dict[str, str | int | None]:
        return {
            "correlation_id": str(self.correlation_id),
            "causation_id": str(self.causation_id),
            "timestamp_ms": int(self.timestamp_ms),
            "tenant_id": str(self.tenant_id) if self.tenant_id is not None else None,
        }