"""
GA Enterprise Core — Guards (Pure Governance Logic)

LAYER: L3

Purpose:
- Preconditions (deterministic guardrails)
- Idempotency (pure state transitions)
- Rate limiting (pure token bucket)
- Circuit breaker (pure closed/open/half-open logic)

Rules:
- No globals / no thread-locals
- No IO / no logging / no async / no threads
- Deterministic, replay-safe
"""

from .circuit_breaker import (
    CircuitPolicy,
    CircuitSnapshot,
    CircuitState,
    can_execute,
    record_failure,
    record_success,
)
from .idempotency import (
    IdempotencyRecord,
    IdempotencyStatus,
    idempotency_complete,
    idempotency_reject,
    idempotency_start,
    is_replay_of,
)
from .preconditions import (
    require,
    require_allowed,
    require_equal,
    require_non_empty_str,
    require_present,
)
from .rate_limit import (
    TokenBucketPolicy,
    TokenBucketState,
    try_consume,
)

__all__ = [
    "require",
    "require_present",
    "require_non_empty_str",
    "require_equal",
    "require_allowed",
    "IdempotencyStatus",
    "IdempotencyRecord",
    "idempotency_start",
    "idempotency_complete",
    "idempotency_reject",
    "is_replay_of",
    "TokenBucketPolicy",
    "TokenBucketState",
    "try_consume",
    "CircuitState",
    "CircuitPolicy",
    "CircuitSnapshot",
    "can_execute",
    "record_success",
    "record_failure",
]
