"""
AfriHome Control Plane — Governance · Usage (Phase 1.7)

Pure, deterministic usage accounting:

- UsageEvent       : immutable event (feature_key, metric_key, quantity, actor)
- Windowing        : pure time windows (minute/hour/day)
- UsageCounter     : immutable per-window counter (fold events)
- UsageAggregate   : immutable roll-up over a time range

No I/O or persistence here. Application/infra layers will store/query counters.
"""
from .usage_event import UsageEvent
from .windowing import UsageGranularity, window_size_ms, window_start_ms, window_end_ms
from .usage_counter import UsageCounter
from .usage_aggregate import UsageAggregate, aggregate_counters

__all__ = [
    "UsageEvent",
    "UsageGranularity",
    "window_size_ms",
    "window_start_ms",
    "window_end_ms",
    "UsageCounter",
    "UsageAggregate",
    "aggregate_counters",
]