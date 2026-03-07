
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

from .registry import (
    HealthStatus,
    HealthCheckResult,
    HealthCheck,
    HealthRegistry,
)
from .diagnostics import (
    DiagnosticReport,
    summarize_status,
    run_diagnostics,
)

__all__ = [
    "HealthStatus", "HealthCheckResult", "HealthCheck", "HealthRegistry",
    "DiagnosticReport", "summarize_status", "run_diagnostics",
]
