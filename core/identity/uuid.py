"""
GA Enterprise Core — Deterministic UUID Authority
-------------------------------------------------

LAYER: L0
Dependencies: stdlib + core.errors + core.typing

Randomness: FORBIDDEN
Time access: FORBIDDEN
Global state: NONE
"""

import hashlib
import uuid
from typing import Final, Protocol, runtime_checkable

from core.errors import InvariantViolationError
from core.typing import (
    AggregateId,
    CausationId,
    CorrelationId,
    EventId,
)

# ============================================================
# UUID Provider Protocol
# ============================================================


@runtime_checkable
class UUIDProvider(Protocol):
    def new_event_id(self) -> EventId: ...
    def new_aggregate_id(self) -> AggregateId: ...
    def new_correlation_id(self) -> CorrelationId: ...
    def new_causation_id(self) -> CausationId: ...


UuidProvider = UUIDProvider


# ============================================================
# Deterministic UUID Provider
# ============================================================


class DeterministicUUIDProvider:
    """
    Deterministic UUIDv5 generator.

    Guarantees
    ----------
    - deterministic across runs
    - unique per call
    - replay safe
    - no randomness
    - no time dependency
    """

    __slots__ = (
        "_seed",
        "_event_counter",
        "_aggregate_counter",
        "_correlation_counter",
        "_causation_counter",
    )

    _NAMESPACE: Final[uuid.UUID] = uuid.UUID("12345678-1234-5678-1234-567812345678")

    def __init__(self, seed: str) -> None:
        if not seed:
            raise InvariantViolationError("UUID seed must be non-empty")

        self._seed = seed

        self._event_counter = 0
        self._aggregate_counter = 0
        self._correlation_counter = 0
        self._causation_counter = 0

    def _derive(self, name: str, counter: int) -> str:

        base = f"{self._seed}:{name}:{counter}"

        digest = hashlib.sha256(base.encode("utf-8")).hexdigest()

        return str(uuid.uuid5(self._NAMESPACE, digest))

    def new_event_id(self) -> EventId:

        self._event_counter += 1

        return EventId(self._derive("event", self._event_counter))

    def new_aggregate_id(self) -> AggregateId:

        self._aggregate_counter += 1

        return AggregateId(self._derive("aggregate", self._aggregate_counter))

    def new_correlation_id(self) -> CorrelationId:

        self._correlation_counter += 1

        return CorrelationId(self._derive("correlation", self._correlation_counter))

    def new_causation_id(self) -> CausationId:

        self._causation_counter += 1

        return CausationId(self._derive("causation", self._causation_counter))


__all__ = [
    "UUIDProvider",
    "UuidProvider",
    "DeterministicUUIDProvider",
]
