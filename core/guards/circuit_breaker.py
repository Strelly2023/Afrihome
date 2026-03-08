"""
GA Enterprise Core — Circuit Breaker (Pure)
-------------------------------------------

LAYER: L3
Dependencies:
- core.typing (UnixMillis)
- core.errors (InvariantViolationError)

Rules:
- No globals / no IO / no threads
- Deterministic state transitions (time injected)
"""

from dataclasses import dataclass
from enum import Enum, auto

from core.errors import InvariantViolationError
from core.typing import UnixMillis


class CircuitState(Enum):
    CLOSED = auto()
    OPEN = auto()
    HALF_OPEN = auto()


@dataclass(frozen=True, slots=True)
class CircuitPolicy:
    failure_threshold: int = 5
    open_duration_ms: int = 30_000
    half_open_max_calls: int = 1
    half_open_successes_to_close: int = 1


@dataclass(frozen=True, slots=True)
class CircuitSnapshot:
    state: CircuitState = CircuitState.CLOSED
    opened_ms: UnixMillis = 0
    consecutive_failures: int = 0
    half_open_inflight: int = 0
    half_open_successes: int = 0


def _to_open(now_ms: UnixMillis, snap: CircuitSnapshot) -> CircuitSnapshot:
    return CircuitSnapshot(
        state=CircuitState.OPEN, opened_ms=now_ms, consecutive_failures=snap.consecutive_failures
    )


def _to_half_open(now_ms: UnixMillis) -> CircuitSnapshot:
    return CircuitSnapshot(state=CircuitState.HALF_OPEN, opened_ms=now_ms)


def _to_closed() -> CircuitSnapshot:
    return CircuitSnapshot(state=CircuitState.CLOSED, opened_ms=0)


def can_execute(
    snap: CircuitSnapshot, now_ms: UnixMillis, policy: CircuitPolicy
) -> tuple[CircuitSnapshot, bool]:
    if now_ms < 0:
        raise InvariantViolationError("now_ms cannot be negative")
    if snap.state is CircuitState.CLOSED:
        return snap, True
    if snap.state is CircuitState.OPEN:
        if now_ms - snap.opened_ms >= policy.open_duration_ms:
            ns = _to_half_open(now_ms)
            if policy.half_open_max_calls <= 0:
                return ns, False
            return (
                CircuitSnapshot(
                    state=CircuitState.HALF_OPEN,
                    opened_ms=ns.opened_ms,
                    consecutive_failures=0,
                    half_open_inflight=1,
                    half_open_successes=0,
                ),
                True,
            )
        return snap, False
    if snap.half_open_inflight < policy.half_open_max_calls:
        return (
            CircuitSnapshot(
                state=CircuitState.HALF_OPEN,
                opened_ms=snap.opened_ms,
                consecutive_failures=snap.consecutive_failures,
                half_open_inflight=snap.half_open_inflight + 1,
                half_open_successes=snap.half_open_successes,
            ),
            True,
        )
    return snap, False


def record_success(
    snap: CircuitSnapshot, now_ms: UnixMillis, policy: CircuitPolicy
) -> CircuitSnapshot:
    if snap.state is CircuitState.CLOSED:
        return CircuitSnapshot(
            state=CircuitState.CLOSED,
            opened_ms=0,
            consecutive_failures=0,
            half_open_inflight=0,
            half_open_successes=0,
        )
    if snap.state is CircuitState.OPEN:
        return snap
    successes = snap.half_open_successes + 1
    inflight = max(0, snap.half_open_inflight - 1)
    if successes >= policy.half_open_successes_to_close:
        return _to_closed()
    return CircuitSnapshot(
        state=CircuitState.HALF_OPEN,
        opened_ms=snap.opened_ms,
        consecutive_failures=0,
        half_open_inflight=inflight,
        half_open_successes=successes,
    )


def record_failure(
    snap: CircuitSnapshot, now_ms: UnixMillis, policy: CircuitPolicy
) -> CircuitSnapshot:
    if snap.state is CircuitState.CLOSED:
        fails = snap.consecutive_failures + 1
        if fails >= policy.failure_threshold:
            return _to_open(
                now_ms,
                CircuitSnapshot(
                    state=snap.state, opened_ms=snap.opened_ms, consecutive_failures=fails
                ),
            )
        return CircuitSnapshot(
            state=CircuitState.CLOSED,
            opened_ms=0,
            consecutive_failures=fails,
            half_open_inflight=0,
            half_open_successes=0,
        )
    if snap.state is CircuitState.OPEN:
        return snap
    inflight = max(0, snap.half_open_inflight - 1)
    _ = inflight
    return _to_open(now_ms, snap)
