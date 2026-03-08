"""
GA Enterprise Core — Health (In-Memory, Deterministic)

LAYER: L3

Purpose:
- In-memory health registry
- Deterministic diagnostics report
- No IO / No threads / No async / No logging

Notes:
- Timestamps are injected by the caller (replay-safe).
- Deterministic ordering (registration order).
"""

from .diagnostics import (
    DiagnosticReport,
    run_diagnostics,
    summarize_status,
)
from .registry import (
    HealthCheck,
    HealthCheckResult,
    HealthRegistry,
    HealthStatus,
)

__all__ = [
    "HealthStatus",
    "HealthCheckResult",
    "HealthCheck",
    "HealthRegistry",
    "DiagnosticReport",
    "summarize_status",
    "run_diagnostics",
]
