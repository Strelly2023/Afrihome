from __future__ import annotations

"""
AfriTech Core Events â€” Event Envelope (GA-Sealed)

This module defines the immutable envelope that combines event metadata
(EventHeaders) with an event fact (DomainEvent).

The EventEnvelope is the canonical, complete representation of an event
within AfriTech's core semantics.

PURPOSE:
- Bind event facts to their immutable metadata
- Provide a stable, replay-safe event record
- Decouple event meaning from transport and execution

RULES:
- Pure data ONLY
- NO execution
- NO IO
- NO time generation
- NO publishing or routing logic
- MUST be immutable

Any change requires an ADR.
"""

from dataclasses import dataclass

from afritech.platform.core.events.base import DomainEvent
from afritech.platform.core.events.headers import EventHeaders


# ============================================================================
# Event Envelope (Immutable Record)
# ============================================================================

@dataclass(frozen=True, slots=True)
class EventEnvelope:
    """
    Immutable event envelope.

    An EventEnvelope represents a complete, self-contained event record,
    consisting of:
    - immutable metadata headers
    - an immutable domain event fact

    It does NOT:
    - publish or dispatch events
    - enforce ordering or delivery semantics
    - reference infrastructure or messaging systems
    - mutate event contents

    Transport, persistence, and consumption are handled
    outside core.
    """

    headers: EventHeaders
    event: DomainEvent
