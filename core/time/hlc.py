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

from __future__ import annotations

from dataclasses import dataclass
from functools import total_ordering

from core.errors import InvariantViolationError
from core.typing import UnixMillis

# ---------- Explicit HLC (injected time) ----------


@dataclass(frozen=True, slots=True)
class HLC:
    """
    Hybrid Logical Clock state (explicit/injected time form).

    physical: Unix milliseconds (injected, NOT read from system)
    logical : logical counter (non-negative)
    """

    physical: UnixMillis
    logical: int

    def __post_init__(self) -> None:
        if self.physical < 0:
            raise InvariantViolationError("Physical time cannot be negative")
        if self.logical < 0:
            raise InvariantViolationError("Logical counter cannot be negative")

    def tick(self, now: UnixMillis) -> "HLC":
        """
        Advance locally with injected 'now':
          - If now > physical  -> (now, 0)
          - Else               -> (physical, logical + 1)
        """
        if now < 0:
            raise InvariantViolationError("Time cannot be negative")
        if now > self.physical:
            return HLC(now, 0)
        return HLC(self.physical, self.logical + 1)

    def merge(self, remote: "HLC", now: UnixMillis) -> "HLC":
        """
        Merge with a remote HLC at injected 'now' (classic HLC rule):
          - physical := max(self.physical, remote.physical, now)
          - if all equal: logical := max(self.logical, remote.logical) + 1
          - if self has max: logical := self.logical + 1
          - if remote has max: logical := remote.logical + 1
          - if now is strictly greatest: logical := 0
        """
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


# ---------- Pure wrapper (test surface): HybridLogicalClock ----------


@total_ordering
@dataclass(frozen=True, slots=True)
class HybridLogicalClock:
    """
    Pure, no-IO HLC wrapper used by tests:
      - __init__(physical: int = 0, logical: int = 0)
      - tick(): monotonic local progression
      - total ordering by (physical, logical)
    It never reads system time. For call-sites with injected time,
    use the explicit 'HLC' type above.
    """

    _state: HLC

    def __init__(self, physical: UnixMillis = 0, logical: int = 0) -> None:
        object.__setattr__(self, "_state", HLC(physical, logical))

    # Minimal test API
    def tick(self) -> "HybridLogicalClock":
        # Pure tick: keep physical baseline; bump logical
        s = self._state
        return HybridLogicalClock(s.physical, s.logical + 1)

    # Optional helpers for advanced users (remain pure)
    def tick_at(self, now: UnixMillis) -> "HybridLogicalClock":
        return HybridLogicalClock.from_hlc(self._state.tick(now))

    def merge(self, other: "HybridLogicalClock") -> "HybridLogicalClock":
        # Pure merge without 'now': max physical determines the bump path
        a, b = self._state, other._state
        max_physical = max(a.physical, b.physical)
        if max_physical == a.physical == b.physical:
            return HybridLogicalClock(max_physical, max(a.logical, b.logical) + 1)
        if max_physical == a.physical:
            return HybridLogicalClock(max_physical, a.logical + 1)
        return HybridLogicalClock(max_physical, b.logical + 1)

    def merge_at(self, other: "HybridLogicalClock", now: UnixMillis) -> "HybridLogicalClock":
        return HybridLogicalClock.from_hlc(self._state.merge(other._state, now))

    # Ordering & equality by (physical, logical)
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, HybridLogicalClock):
            return NotImplemented
        return (self._state.physical, self._state.logical) == (
            other._state.physical,
            other._state.logical,
        )

    def __lt__(self, other: "HybridLogicalClock") -> bool:
        return (self._state.physical, self._state.logical) < (
            other._state.physical,
            other._state.logical,
        )

    # Read-only accessors
    @property
    def physical(self) -> UnixMillis:
        return self._state.physical

    @property
    def logical(self) -> int:
        return self._state.logical

    @staticmethod
    def from_hlc(hlc: HLC) -> "HybridLogicalClock":
        return HybridLogicalClock(hlc.physical, hlc.logical)


__all__ = ["HLC", "HybridLogicalClock"]
