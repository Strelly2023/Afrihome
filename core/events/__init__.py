# core/events/__init__.py
"""
GA Enterprise Core — Event Spine

LAYER: L2

Purpose:
- Immutable domain events
- Canonical event envelopes
- Deterministic hashing
- In-process dispatcher (no IO)
"""

from core.typing import EventId  # <-- re-export EventId for tests

from .bus import InProcessEventBus
from .envelope import EventEnvelope
from .event import DomainEvent
from .headers import EventHeaders

__all__ = [
    "EventId",
    "DomainEvent",
    "EventHeaders",
    "EventEnvelope",
    "InProcessEventBus",
]
