"""
GA Enterprise Core â€” Time Public API
-----------------------------------

LAYER: L1 (Foundation)
Deterministic: YES
Side effects: NONE

This package defines the canonical, GAâ€‘stable time primitives
used throughout afritech.platform.core.

Rules:
- No system time access
- All time MUST be injected via Clock
- Implementations here are deterministic only
"""

from .clock import Clock
from .fixed import FixedClock
from .hlc import HLC


__all__ = [
    "Clock",
    "FixedClock",
    "HLC",
]
