from enum import Enum, auto

from core.typing import UnixMillis


class UsageGranularity(Enum):
    MINUTE = auto()
    HOUR = auto()
    DAY = auto()
    # (If you ever add MONTH, prefer a (year, month) key to avoid TZ pitfalls in governance)


def window_size_ms(granularity: UsageGranularity) -> int:
    if granularity is UsageGranularity.MINUTE:
        return 60_000
    if granularity is UsageGranularity.HOUR:
        return 3_600_000
    if granularity is UsageGranularity.DAY:
        return 86_400_000
    raise ValueError(f"Unsupported granularity: {granularity}")


def window_start_ms(ts: UnixMillis, granularity: UsageGranularity) -> UnixMillis:
    """
    Deterministic floor to the start of the window in UTC milliseconds.
    No ambient clock reads; purely derived from ts.
    """
    sz = window_size_ms(granularity)
    return UnixMillis(int(ts) // sz * sz)


def window_end_ms(start: UnixMillis, granularity: UsageGranularity) -> UnixMillis:
    return UnixMillis(int(start) + window_size_ms(granularity))
