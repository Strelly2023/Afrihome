
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

from .preconditions import (
    require,
    require_present,
    require_non_empty_str,
    require_equal,
    require_allowed,
)
from .idempotency import (
    IdempotencyStatus,
    IdempotencyRecord,
    idempotency_start,
    idempotency_complete,
    idempotency_reject,
    is_replay_of,
)
from .rate_limit import (
    TokenBucketPolicy,
    TokenBucketState,
    try_consume,
)
from .circuit_breaker import (
    CircuitState,
    CircuitPolicy,
    CircuitSnapshot,
    can_execute,
    record_success,
    record_failure,
)

__all__ = [
    "require", "require_present", "require_non_empty_str", "require_equal", "require_allowed",
    "IdempotencyStatus", "IdempotencyRecord", "idempotency_start", "idempotency_complete", "idempotency_reject", "is_replay_of",
    "TokenBucketPolicy", "TokenBucketState", "try_consume",
    "CircuitState", "CircuitPolicy", "CircuitSnapshot", "can_execute", "record_success", "record_failure",
]
