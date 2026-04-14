from __future__ import annotations

"""
AfriTech Core Events â€” Event Headers (GA-Sealed)

This module defines the immutable metadata headers that accompany
all domain events in the AfriTech platform.

Event headers provide contextual identification and correlation
for events WITHOUT introducing execution, timing, or transport
authority into the core.

PURPOSE:
- Provide a canonical, stable metadata shape for events
- Enable deterministic replay and audit
- Decouple event facts from infrastructure concerns

RULES:
- Pure data ONLY
- NO execution
- NO IO
- NO time generation
- NO publishing or routing logic
- MUST be immutable

Any change requires an ADR.
"""

from dataclasses import dataclass, field
from typing import Mapping, Any
from types import MappingProxyType


# ============================================================================
# Event Headers (Immutable Metadata)
# ============================================================================

@dataclass(frozen=True, slots=True)
class EventHeaders:
    """
    Immutable event metadata headers.

    EventHeaders capture contextual identifiers associated
    with a domain event.

    They define:
    - a stable event identifier
    - the event occurrence timestamp (injected externally)
    - the logical source of the event
    - a correlation identifier for tracing
    - opaque, structured attributes

    They do NOT:
    - generate time
    - allocate identifiers
    - publish events
    - reference infrastructure
    - enforce semantics
    """

    event_id: str
    occurred_at_ms: int
    source: str
    correlation_id: str
    attributes: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )

    # ------------------------------------------------------------------
    # Post-init normalization (deep immutability guarantee)
    # ------------------------------------------------------------------

    def __post_init__(self) -> None:
        """
        Ensure attributes are deeply immutable, even if a mutable
        mapping is provided by the caller.
        """
        object.__setattr__(
            self,
            "attributes",
            MappingProxyType(dict(self.attributes)),
        )
