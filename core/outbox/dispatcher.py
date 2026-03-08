"""
GA Enterprise Core — Outbox Dispatcher (Pure State)
---------------------------------------------------

LAYER: L2
Dependencies:
- core.outbox.store_protocol
- core.outbox.model
- core.outbox.backoff
- core.events.envelope
- core.kernel.invariants
- core.typing

Rules:
- No IO
- No threads/async
- Deterministic ordering
"""

from dataclasses import dataclass
from typing import List

from core.events.envelope import EventEnvelope
from core.kernel.invariants import assert_not_none, assert_true
from core.outbox.backoff import BackoffPolicy, compute_backoff_ms
from core.outbox.model import OutboxRecord, OutboxStatus
from core.outbox.store_protocol import OutboxStore
from core.typing import EventId, UnixMillis

# ----------------------
# Immutable DTOs (L2)
# ----------------------


@dataclass(frozen=True, slots=True)
class DispatchItem:
    event_id: EventId
    topic: str
    envelope: EventEnvelope


@dataclass(frozen=True, slots=True)
class DispatchPlan:
    items: List[DispatchItem]


# ----------------------
# Pure Dispatcher Logic
# ----------------------


def plan_dispatch(
    store: OutboxStore,
    topic: str,
    now_ms: UnixMillis,
    limit: int,
) -> DispatchPlan:
    assert_not_none(store, "store")
    assert_not_none(topic, "topic")
    assert_not_none(now_ms, "now_ms")
    assert_true(limit > 0, "limit must be positive")

    eligible = store.get_eligible(topic, now_ms, limit)
    items = [DispatchItem(r.event_id, r.topic, r.envelope) for r in eligible]
    return DispatchPlan(items=items)


def apply_success(store: OutboxStore, event_id: EventId) -> OutboxRecord:
    rec = store.get(event_id)
    assert_not_none(rec, "record")
    assert_true(
        rec.status is OutboxStatus.PENDING,
        "cannot dispatch non-pending record",
    )

    updated = rec.mark_dispatched()
    store.put(updated)
    return updated


def apply_failure(
    store: OutboxStore,
    event_id: EventId,
    now_ms: UnixMillis,
    policy: BackoffPolicy = BackoffPolicy(),
    error: str | None = None,
) -> OutboxRecord:
    rec = store.get(event_id)
    assert_not_none(rec, "record")
    assert_true(
        rec.status is OutboxStatus.PENDING,
        "cannot fail non-pending record",
    )

    next_delay = compute_backoff_ms(rec.attempts + 1, policy)
    updated = rec.schedule_retry(
        now_ms=now_ms,
        next_delay_ms=next_delay,
        error=error,
    )
    store.put(updated)
    return updated
