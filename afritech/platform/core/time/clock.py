from __future__ import annotations
"""
GA Enterprise Core â€” Clock Abstraction
-------------------------------------

LAYER: L1 (Foundation)
Dependencies: stdlib, core.typing only
Deterministic: YES
Side effects: NONE

Purpose:
- Define the canonical Clock contract
- Enforce explicit, injected time across the core

Rules:
- NO system time access
- NO datetime / time imports
- NO mutation semantics
- Infrastructure clocks live OUTSIDE core
"""
#afritch/platform/core/time/clock.py

from typing import Protocol, runtime_checkable

from afritech.platform.core.typing import UnixMillis


@runtime_checkable
class Clock(Protocol):
    """
    Deterministic clock contract.

    Implementations MUST:
    - return UnixMillis
    - be deterministic
    - have no implicit side effects

    Implementations MUST NOT:
    - access system time
    - perform IO
    - introduce hidden state
    """

    def now_ms(self) -> UnixMillis:
        """Return the current time in Unix milliseconds."""
        ...
