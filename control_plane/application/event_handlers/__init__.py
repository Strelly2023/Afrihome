"""
AfriHome Control Plane — Application/Event Handlers
PHASE: 3.12 (Orchestration only)
IO: NONE | Threads/async: NONE | Deterministic: YES

Exports:
- ReactionPlan, OutboxWrite
- EventReaction, OutboxWriter
- EventBuilder
- EventRouter
- EventHandlingService
"""

from .builder import EventBuilder
from .models import OutboxWrite, ReactionPlan
from .protocols import EventReaction, OutboxWriter
from .router import EventRouter
from .service import EventHandlingService

__all__ = [
    "ReactionPlan",
    "OutboxWrite",
    "EventReaction",
    "OutboxWriter",
    "EventBuilder",
    "EventRouter",
    "EventHandlingService",
]
