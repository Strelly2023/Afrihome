# afritech/platform/control_plane/time/clock.py
"""
DEPRECATED — CLOCKS MUST NOT LIVE IN CORE

This module exists only to prevent silent governance violations.

Clocks are environmental concerns and MUST be injected from
non-Core layers.

See:
- ADR-KE-FT-001 — Clock / Time Injection Enforcement
"""

raise RuntimeError(
    "Clock MUST NOT be imported from afritech.platform.core.time.clock. "
    "Use afritech.platform.control_plane.time.clock instead."
)