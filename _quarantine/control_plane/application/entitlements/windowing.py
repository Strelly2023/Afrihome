from dataclasses import dataclass
from datetime import datetime, timezone
from calendar import monthrange
from core.errors import InvariantViolationError
from core.kernel.invariants import assert_not_none
from .protocols import WindowCalculator, WindowKind

@dataclass(frozen=True, slots=True)
class FixedWindowCalculator(WindowCalculator):
    """
    Deterministic, dependency-free window calculator.
    Uses UTC boundaries. No IO/ambient time; 'now_ms' is injected by caller.
    """
    def compute(self, *, now_ms: int, window: str) -> tuple[str, int, int]:
        assert_not_none(now_ms, "now_ms")
        if now_ms < 0:
            raise InvariantViolationError("now_ms cannot be negative")
        if window not in {
            WindowKind.FIXED_MINUTE, WindowKind.FIXED_HOUR, WindowKind.FIXED_DAY, WindowKind.FIXED_MONTH
        }:
            raise InvariantViolationError(f"Unsupported window kind: {window!r}")

        dt = datetime.fromtimestamp(now_ms / 1000, tz=timezone.utc)

        if window == WindowKind.FIXED_MINUTE:
            start = dt.replace(second=0, microsecond=0)
            end = start.replace(second=59, microsecond=999000)
            wid = start.strftime("m:%Y%m%d%H%M")
        elif window == WindowKind.FIXED_HOUR:
            start = dt.replace(minute=0, second=0, microsecond=0)
            end = start.replace(minute=59, second=59, microsecond=999000)
            wid = start.strftime("h:%Y%m%d%H")
        elif window == WindowKind.FIXED_DAY:
            start = dt.replace(hour=0, minute=0, second=0, microsecond=0)
            end = start.replace(hour=23, minute=59, second=59, microsecond=999000)
            wid = start.strftime("d:%Y%m%d")
        else:  # FIXED_MONTH
            start = dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            last_day = monthrange(dt.year, dt.month)[1]
            end = start.replace(day=last_day, hour=23, minute=59, second=59, microsecond=999000)
            wid = start.strftime("M:%Y%m")

        start_ms = int(start.timestamp() * 1000)
        end_ms = int(end.timestamp() * 1000)
        return wid, start_ms, end_ms