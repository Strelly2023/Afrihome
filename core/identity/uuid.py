
"""
GA Enterprise Core — Deterministic UUID Authority
-------------------------------------------------

LAYER: L0
Dependencies: stdlib + core.errors + core.typing
Randomness: FORBIDDEN
Time access: FORBIDDEN
Global state: NONE

Rules:
- Models must NEVER generate UUIDs.
- UUIDs must be injected.
- Default implementation must be deterministic.
"""


import hashlib
import uuid
from typing import Protocol, runtime_checkable, Final

from core.errors import InvariantViolationError
from core.typing import (
    EventId,
    AggregateId,
    CorrelationId,
    CausationId,
)


# ============================================================
# UUID Provider Protocol
# ============================================================

@runtime_checkable
class UUIDProvider(Protocol):
    """
    Deterministic UUID provider contract.

    Implementations must be:
    - Pure
    - Deterministic
    - Side-effect free
    """

    def new_event_id(self) -> EventId: ...
    def new_aggregate_id(self) -> AggregateId: ...
    def new_correlation_id(self) -> CorrelationId: ...
    def new_causation_id(self) -> CausationId: ...

# Compatibility alias
UuidProvider = UUIDProvider

# ============================================================
# Deterministic Namespace Provider
# ============================================================

class DeterministicUUIDProvider:
    """
    Deterministic UUIDv5-based provider.

    Requires explicit seed.
    No randomness.
    No global counters.
    """

    _NAMESPACE: Final[uuid.UUID] = uuid.UUID("12345678-1234-5678-1234-567812345678")

    def __init__(self, seed: str) -> None:
        if not seed:
            raise InvariantViolationError("UUID seed must be non-empty")
        self._seed = seed

    def _derive(self, name: str) -> str:
        full = f"{self._seed}:{name}"
        digest = hashlib.sha256(full.encode("utf-8")).hexdigest()
        return str(uuid.uuid5(self._NAMESPACE, digest))

    def new_event_id(self) -> EventId:
        return EventId(self._derive("event"))

    def new_aggregate_id(self) -> AggregateId:
        return AggregateId(self._derive("aggregate"))

    def new_correlation_id(self) -> CorrelationId:
        return CorrelationId(self._derive("correlation"))

    def new_causation_id(self) -> CausationId:
        return CausationId(self._derive("causation"))


__all__ = [
    "UUIDProvider",
    "UuidProvider",
    "DeterministicUUIDProvider",
]
