
"""
GA Enterprise Core — Hybrid Logical Clock (HLC)
-----------------------------------------------

LAYER: L0
Dependencies: core.typing + core.errors
System time access: NONE
Threading: NONE
IO: NONE

Purpose:
- Provide causal ordering
- Combine physical time + logical counter
- Deterministic state transitions
"""


from dataclasses import dataclass

from core.typing import UnixMillis
from core.errors import InvariantViolationError


@dataclass(frozen=True, slots=True)
class HLC:
    """
    Hybrid Logical Clock state.

    physical: Unix milliseconds
    logical: logical counter
    """

    physical: UnixMillis
    logical: int

    def __post_init__(self) -> None:
        if self.physical < 0:
            raise InvariantViolationError("Physical time cannot be negative")
        if self.logical < 0:
            raise InvariantViolationError("Logical counter cannot be negative")

    def tick(self, now: UnixMillis) -> "HLC":
        if now < 0:
            raise InvariantViolationError("Time cannot be negative")
        if now > self.physical:
            return HLC(now, 0)
        return HLC(self.physical, self.logical + 1)

    def merge(self, remote: "HLC", now: UnixMillis) -> "HLC":
        if now < 0:
            raise InvariantViolationError("Time cannot be negative")
        max_physical = max(self.physical, remote.physical, now)
        if max_physical == self.physical == remote.physical:
            return HLC(max_physical, max(self.logical, remote.logical) + 1)
        if max_physical == self.physical:
            return HLC(max_physical, self.logical + 1)
        if max_physical == remote.physical:
            return HLC(max_physical, remote.logical + 1)
        return HLC(max_physical, 0)


__all__ = ["HLC"]
