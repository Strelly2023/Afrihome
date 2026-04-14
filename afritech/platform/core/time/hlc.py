from __future__ import annotations

"""
GA Enterprise Core â€” Hybrid Logical Clock (HLC)
-----------------------------------------------

LAYER: L1 (Foundation)
Dependencies: core.typing + core.errors.base + stdlib
Deterministic: YES
System time access: NONE
Threading: NONE
IO: NONE

Purpose:
- Represent causal ordering state
- Combine physical time (UnixMillis) with a logical counter
- Provide pure, deterministic state transitions

Rules:
- Immutable value object
- No randomness, no clocks
- All time is injected explicitly
- Temporal invariants MUST raise InvariantViolationError
"""

from dataclasses import dataclass

from afritech.platform.core.typing import UnixMillis
from afritech.platform.core.errors.base import InvariantViolationError


# ============================================================
# Hybrid Logical Clock Value
# ============================================================

@dataclass(frozen=True, slots=True)
class HLC:
    """
    Hybrid Logical Clock state.

    Fields:
    - physical: UnixMillis (injected time)
    - logical: logical counter

    This type is:
    - immutable
    - deterministic
    - replayâ€‘safe
    """

    physical: UnixMillis
    logical: int

    def __post_init__(self) -> None:
        if int(self.physical) < 0:
            raise InvariantViolationError(
                "HLC physical time must be non-negative",
                metadata={"physical": int(self.physical)},
            )

        if self.logical < 0:
            raise InvariantViolationError(
                "HLC logical counter must be non-negative",
                metadata={"logical": self.logical},
            )

    # --------------------------------------------------------
    # Local tick
    # --------------------------------------------------------

    def tick(self, now: UnixMillis) -> "HLC":
        """
        Advance the clock for a local event.

        Rules:
        - If injected time moves forward â†’ reset logical counter
        - Otherwise â†’ increment logical counter
        """
        if int(now) < 0:
            raise InvariantViolationError(
                "HLC time must be non-negative",
                metadata={"now": int(now)},
            )

        if now > self.physical:
            return HLC(now, 0)

        return HLC(self.physical, self.logical + 1)

    # --------------------------------------------------------
    # Merge with remote clock
    # --------------------------------------------------------

    def merge(self, remote: "HLC", now: UnixMillis) -> "HLC":
        """
        Merge this clock with a remote clock.

        Rules (standard HLC semantics):
        - physical := max(local.physical, remote.physical, now)
        - logical counter follows causal precedence rules
        """
        if int(now) < 0:
            raise InvariantViolationError(
                "HLC time must be non-negative",
                metadata={"now": int(now)},
            )

        max_physical = max(self.physical, remote.physical, now)

        if max_physical == self.physical == remote.physical:
            return HLC(
                max_physical,
                max(self.logical, remote.logical) + 1,
            )

        if max_physical == self.physical:
            return HLC(max_physical, self.logical + 1)

        if max_physical == remote.physical:
            return HLC(max_physical, remote.logical + 1)

        return HLC(max_physical, 0)


# ============================================================
# HLC ABI (explicit, frozen)
# ============================================================

__all__ = ["HLC"]
