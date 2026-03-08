from typing import Protocol, runtime_checkable


@runtime_checkable
class WindowCalculator(Protocol):
    """
    Pure window calculator contract.
    Returns: (window_id, window_start_ms, window_end_ms)
    """

    def compute(self, *, now_ms: int, window: str) -> tuple[str, int, int]: ...


# Window kind constants (shared semantic surface)
WINDOW_MINUTE = "fixed_minute"
WINDOW_HOUR = "fixed_hour"
WINDOW_DAY = "fixed_day"
WINDOW_MONTH = "fixed_month"
