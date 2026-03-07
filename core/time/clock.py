
"""
GA Enterprise Core — Clock Authority
-------------------------------------

LAYER: L0
Dependencies: stdlib + core.typing + core.errors
System time access: FORBIDDEN inside models
Deterministic: YES

Rules:
- Time must be injected.
- No datetime.now() in models.
"""


import time
from typing import Protocol, runtime_checkable

from core.typing import UnixMillis
from core.errors import InvariantViolationError


@runtime_checkable
class Clock(Protocol):
    """
    Deterministic clock contract.
    """

    def now_ms(self) -> UnixMillis: ...


class SystemClock:
    """
    Real system clock.

    NOTE:
    - May only be instantiated at infrastructure boundary.
    - Never inside models.
    """

    def now_ms(self) -> UnixMillis:
        return UnixMillis(int(time.time() * 1000))


class FixedClock:
    """
    Always returns the same timestamp.
    Fully deterministic.
    """

    def __init__(self, fixed_time: UnixMillis) -> None:
        if fixed_time < 0:
            raise InvariantViolationError("Time cannot be negative")
        self._fixed_time = fixed_time

    def now_ms(self) -> UnixMillis:
        return self._fixed_time


__all__ = [
    "Clock",
    "SystemClock",
    "FixedClock",
]
