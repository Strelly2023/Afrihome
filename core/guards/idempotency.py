"""
GA Enterprise Core — Idempotency (Pure Transitions)
---------------------------------------------------

LAYER: L3
Dependencies:
- core.typing (UnixMillis)
- core.errors (InvariantViolationError)
- core.kernel.invariants (assert_not_none)

Rules:
- No globals / no IO
- Immutable records
- Deterministic transitions
"""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional

from core.errors import InvariantViolationError
from core.kernel.invariants import assert_not_none
from core.typing import UnixMillis


class IdempotencyStatus(Enum):
    IN_PROGRESS = auto()
    COMPLETED = auto()
    REJECTED = auto()


@dataclass(frozen=True, slots=True)
class IdempotencyRecord:
    key: str
    status: IdempotencyStatus
    first_seen_ms: UnixMillis
    last_seen_ms: UnixMillis
    response_hash: Optional[str] = None
    reason: Optional[str] = None

    def __post_init__(self) -> None:
        assert_not_none(self.key, "key")
        if self.first_seen_ms < 0 or self.last_seen_ms < 0:
            raise InvariantViolationError("timestamps cannot be negative")


def idempotency_start(
    existing: Optional[IdempotencyRecord], *, key: str, now_ms: UnixMillis
) -> tuple[IdempotencyRecord, bool]:
    if now_ms < 0:
        raise InvariantViolationError("now_ms cannot be negative")

    if existing is None:
        rec = IdempotencyRecord(
            key=key,
            status=IdempotencyStatus.IN_PROGRESS,
            first_seen_ms=now_ms,
            last_seen_ms=now_ms,
        )
        return rec, True

    # Return the same status and metadata, only updating last_seen_ms
    return (
        IdempotencyRecord(
            key=existing.key,
            status=existing.status,
            first_seen_ms=existing.first_seen_ms,
            last_seen_ms=now_ms,
            response_hash=existing.response_hash,
            reason=existing.reason,
        ),
        False,
    )


def idempotency_complete(
    existing: IdempotencyRecord, *, response_hash: str, now_ms: UnixMillis
) -> IdempotencyRecord:
    """Mark request as COMPLETED; preserve existing response_hash if already completed."""
    if now_ms < 0:
        raise InvariantViolationError("now_ms cannot be negative")

    if existing.status is IdempotencyStatus.COMPLETED:
        return IdempotencyRecord(
            key=existing.key,
            status=IdempotencyStatus.COMPLETED,
            first_seen_ms=existing.first_seen_ms,
            last_seen_ms=now_ms,
            response_hash=existing.response_hash or response_hash,
            reason=None,
        )

    return IdempotencyRecord(
        key=existing.key,
        status=IdempotencyStatus.COMPLETED,
        first_seen_ms=existing.first_seen_ms,
        last_seen_ms=now_ms,
        response_hash=response_hash,
        reason=None,
    )


def idempotency_reject(
    existing: IdempotencyRecord | None, *, key: str, reason: str, now_ms: UnixMillis
) -> IdempotencyRecord:
    """Mark request as REJECTED; if no record exists, create one."""
    if now_ms < 0:
        raise InvariantViolationError("now_ms cannot be negative")

    if existing is None:
        return IdempotencyRecord(
            key=key,
            status=IdempotencyStatus.REJECTED,
            first_seen_ms=now_ms,
            last_seen_ms=now_ms,
            response_hash=None,
            reason=reason,
        )

    return IdempotencyRecord(
        key=existing.key,
        status=IdempotencyStatus.REJECTED,
        first_seen_ms=existing.first_seen_ms,
        last_seen_ms=now_ms,
        response_hash=None,
        reason=reason,
    )


def is_replay_of(existing: Optional[IdempotencyRecord], *, response_hash: str | None) -> bool:
    """
    Returns True if:
      - a previous COMPLETED record exists, and
      - response_hash is None (any completed response qualifies), OR
      - response_hash matches the stored response hash.
    """
    if existing is None:
        return False
    if existing.status is not IdempotencyStatus.COMPLETED:
        return False
    if response_hash is None:
        return True
    return existing.response_hash == response_hash
