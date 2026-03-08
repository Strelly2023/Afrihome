
"""
GA Enterprise Core — Outbox Writer
----------------------------------

LAYER: L2
Dependencies:
- core.outbox.topic_grammar
- core.outbox.model
- core.outbox.store_protocol
- core.events.envelope
- core.typing

IO: NONE
"""


from core.outbox.topic_grammar import validate_topic
from core.outbox.model import OutboxRecord
from core.outbox.store_protocol import OutboxStore
from core.events.envelope import EventEnvelope
from core.typing import UnixMillis


def write_outbox_record(
    store: OutboxStore,
    topic: str,
    envelope: EventEnvelope,
    now_ms: UnixMillis,
) -> OutboxRecord:
    t = validate_topic(topic)
    rec = OutboxRecord(
        event_id=envelope.event.event_id,
        topic=t,
        envelope=envelope,
        attempts=0,
        next_attempt_ms=now_ms,
    )
    store.append(rec)
    return rec
