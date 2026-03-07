from dataclasses import dataclass
from typing import Mapping, Any
from core.typing import UnixMillis

@dataclass(frozen=True, slots=True)
class UsageIncrement:
    """
    Immutable request to record usage for a key.
    NOTE: This is orchestration-only: no counters are modified here.
    """
    key: str
    amount: int = 1
    attributes: Mapping[str, Any] = ()

@dataclass(frozen=True, slots=True)
class WindowedUsagePlan:
    """
    Immutable plan describing a usage record bound to a window.
    This is what we embed into the event payload for downstream workers.
    """
    key: str
    amount: int
    window_id: str
    window_start_ms: UnixMillis
    window_end_ms: UnixMillis
    attributes: Mapping[str, Any]