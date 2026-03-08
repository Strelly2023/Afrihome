"""
GA Enterprise Core — Rate Limiting (Pure Token Bucket)
------------------------------------------------------

LAYER: L3
Dependencies:
- core.typing (UnixMillis)
- core.errors (InvariantViolationError)
- core.kernel.invariants (assert_not_none)

Rules:
- No globals / no IO / no threads
- Deterministic refill based on injected timestamps
"""

from dataclasses import dataclass

from core.errors import InvariantViolationError
from core.typing import UnixMillis


@dataclass(frozen=True, slots=True)
class TokenBucketPolicy:
    capacity: int
    refill_rate_per_ms: float


@dataclass(frozen=True, slots=True)
class TokenBucketState:
    tokens: float
    last_refill_ms: UnixMillis


def _refill(
    state: TokenBucketState, now_ms: UnixMillis, policy: TokenBucketPolicy
) -> TokenBucketState:
    if now_ms < state.last_refill_ms:
        raise InvariantViolationError("now_ms must be >= last_refill_ms")
    elapsed = int(now_ms) - int(state.last_refill_ms)
    if elapsed <= 0:
        return state
    new_tokens = min(policy.capacity, state.tokens + elapsed * policy.refill_rate_per_ms)
    return TokenBucketState(tokens=new_tokens, last_refill_ms=now_ms)


def try_consume(
    state: TokenBucketState, now_ms: UnixMillis, policy: TokenBucketPolicy, cost: int = 1
) -> tuple[TokenBucketState, bool]:
    if cost <= 0:
        raise InvariantViolationError("cost must be positive")
    s = _refill(state, now_ms, policy)
    if s.tokens >= cost:
        return TokenBucketState(tokens=s.tokens - cost, last_refill_ms=s.last_refill_ms), True
    return s, False
