
"""
GA Enterprise Core — Deterministic Event Envelope
-------------------------------------------------

LAYER: L2
Dependencies:
- core.events.event
- core.events.headers
- stdlib hashlib/json

Rules:
- Immutable
- Deterministic hash
- Canonical JSON encoding
"""


import hashlib
import json
from dataclasses import dataclass

from core.events.event import DomainEvent
from core.events.headers import EventHeaders
from core.kernel.invariants import assert_not_none


@dataclass(frozen=True, slots=True)
class EventEnvelope:
    """
    Immutable event envelope.

    Combines:
    - DomainEvent
    - EventHeaders
    - Deterministic content hash
    """

    event: DomainEvent
    headers: EventHeaders
    content_hash: str

    def __post_init__(self) -> None:
        assert_not_none(self.event, "event")
        assert_not_none(self.headers, "headers")
        assert_not_none(self.content_hash, "content_hash")

    @staticmethod
    def create(event: DomainEvent, headers: EventHeaders) -> "EventEnvelope":
        canonical = {
            "event": event.to_dict(),
            "headers": headers.to_dict(),
        }
        encoded = json.dumps(canonical, sort_keys=True, separators=(",", ":")).encode("utf-8")
        digest = hashlib.sha256(encoded).hexdigest()
        return EventEnvelope(event=event, headers=headers, content_hash=digest)
