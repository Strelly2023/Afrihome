"""
GA Enterprise Core — Outbox Model
---------------------------------

LAYER: L2
Dependencies: L0+L1 (core.typing, core.errors), core.events
Deterministic: YES
IO: NONE
"""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional

from core.errors import InvariantViolationError
from core.events.envelope import EventEnvelope
from core.typing import EventId, UnixMillis


class OutboxStatus(Enum):
    PENDING = auto()
    DISPATCHED = auto()


@dataclass(frozen=True, slots=True)
class OutboxRecord:
    event_id: EventId
    topic: str
    envelope: EventEnvelope
    attempts: int
    next_attempt_ms: UnixMillis
    status: OutboxStatus = OutboxStatus.PENDING
    last_error: Optional[str] = None

    def __post_init__(self) -> None:
        if self.attempts < 0:
            raise InvariantViolationError("attempts cannot be negative")
        if self.next_attempt_ms < 0:
            raise InvariantViolationError("next_attempt_ms cannot be negative")
        if not self.topic:
            raise InvariantViolationError("topic cannot be empty")

    def mark_dispatched(self) -> "OutboxRecord":
        return OutboxRecord(
            event_id=self.event_id,
            topic=self.topic,
            envelope=self.envelope,
            attempts=self.attempts,
            next_attempt_ms=self.next_attempt_ms,
            status=OutboxStatus.DISPATCHED,
            last_error=None,
        )

    def schedule_retry(
        self, now_ms: UnixMillis, next_delay_ms: int, error: Optional[str]
    ) -> "OutboxRecord":
        if now_ms < 0 or next_delay_ms < 0:
            raise InvariantViolationError("now_ms and next_delay_ms must be non-negative")
        return OutboxRecord(
            event_id=self.event_id,
            topic=self.topic,
            envelope=self.envelope,
            attempts=self.attempts + 1,
            next_attempt_ms=UnixMillis(int(now_ms) + int(next_delay_ms)),
            status=OutboxStatus.PENDING,
            last_error=error,
        )
