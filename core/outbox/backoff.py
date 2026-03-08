"""
GA Enterprise Core — Deterministic Backoff
------------------------------------------

LAYER: L2
Dependencies: stdlib only
Randomness: FORBIDDEN
Sleep: FORBIDDEN
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class BackoffPolicy:
    base_ms: int = 100
    factor: int = 2
    max_ms: int = 60_000


def compute_backoff_ms(attempt: int, policy: BackoffPolicy = BackoffPolicy()) -> int:
    if attempt <= 0:
        return 0
    delay = policy.base_ms * (policy.factor ** (attempt - 1))
    if delay > policy.max_ms:
        delay = policy.max_ms
    return int(delay)
