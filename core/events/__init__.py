
"""
GA Enterprise Core — Event Spine

LAYER: L2

Purpose:
- Immutable domain events
- Canonical event envelopes
- Deterministic hashing
- In-process dispatcher (no IO)
"""

from .event import DomainEvent
from .headers import EventHeaders
from .envelope import EventEnvelope
from .bus import InProcessEventBus

__all__ = [
    "DomainEvent", "EventHeaders", "EventEnvelope", "InProcessEventBus",
]
