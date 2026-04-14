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
from .models import ReactionPlan, OutboxWrite
from .protocols import EventReaction, OutboxWriter
from .builder import EventBuilder
from .router import EventRouter
from .service import EventHandlingService

__all__ = [
    "ReactionPlan", "OutboxWrite",
    "EventReaction", "OutboxWriter",
    "EventBuilder",
    "EventRouter",
    "EventHandlingService",
]