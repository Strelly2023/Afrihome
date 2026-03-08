"""
GA Enterprise Core — Outbox Durability Spine

LAYER: L2

Purpose:
- Canonical topic grammar
- Deterministic outbox record model
- Store protocol (no IO assumptions)
- Deterministic backoff (no sleeps, no randomness)
- Pure dispatcher state machine (plan + apply)
- In-memory store for testing/in-process usage
"""

from .backoff import BackoffPolicy, compute_backoff_ms
from .dispatcher import (
    DispatchItem,
    DispatchPlan,
    apply_failure,
    apply_success,
    plan_dispatch,
)
from .memory_store import InMemoryOutboxStore
from .model import OutboxRecord, OutboxStatus
from .store_protocol import OutboxStore
from .topic_grammar import (
    TOPIC_PATTERN,
    is_valid_topic,
    normalize_topic,
    validate_topic,
)
from .writer import write_outbox_record

__all__ = [
    "normalize_topic",
    "validate_topic",
    "is_valid_topic",
    "TOPIC_PATTERN",
    "OutboxStatus",
    "OutboxRecord",
    "OutboxStore",
    "BackoffPolicy",
    "compute_backoff_ms",
    "write_outbox_record",
    "DispatchItem",
    "DispatchPlan",
    "plan_dispatch",
    "apply_success",
    "apply_failure",
    "InMemoryOutboxStore",
]
