from dataclasses import dataclass

from core.errors import AuthorizationError
from core.typing import UnixMillis


@dataclass(frozen=True, slots=True)
class EntitlementDecision:
    """
    Immutable entitlement check result (pure, no IO).
    """

    key: str
    allowed: bool
    reason: str


@dataclass(frozen=True, slots=True)
class QuotaDecision:
    """
    Immutable quota enforcement result (pure, no IO).
    """

    quota_key: str
    allowed: bool
    used: int
    limit: int
    remaining: int
    window_id: str
    window_start_ms: UnixMillis
    window_end_ms: UnixMillis
    reason: str


class QuotaExceededError(AuthorizationError):
    """
    Raised when callers want an exception-based guard (optional).
    """

    def __init__(self, reason: str = "Quota exceeded"):
        super().__init__(reason)
