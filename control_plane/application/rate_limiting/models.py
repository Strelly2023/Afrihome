from dataclasses import dataclass

from core.typing import UnixMillis


@dataclass(frozen=True, slots=True)
class RateDecision:
    """
    Immutable rate-limit outcome (pure orchestration result).
    The caller decides whether to persist the returned new state (outbox/infra later).
    """

    key: str
    allowed: bool
    reason: str
    cost: int
    tokens_before: float
    tokens_after: float
    last_refill_ms_before: UnixMillis
    last_refill_ms_after: UnixMillis
