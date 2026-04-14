from __future__ import annotations

"""
AfriTech Core Events â€” Base Event (GA-Sealed)

This module defines the base, immutable domain event primitive
used throughout the AfriTech platform.

Events represent *facts that have occurred*.
They are declarative, immutable, and side-effect free.

PURPOSE:
- Provide a canonical base type for all domain events
- Enable deterministic replay and audit
- Establish a stable, engine-agnostic event language

RULES:
- Pure data ONLY
- NO execution
- NO publishing or subscribing
- NO IO
- NO time
- NO infrastructure integration
- MUST be immutable

Any change requires an ADR.
"""

from dataclasses import dataclass, field
from typing import Mapping, Any
from types import MappingProxyType


# ============================================================================
# Base Domain Event (Immutable Fact)
# ============================================================================

@dataclass(frozen=True, slots=True)
class DomainEvent:
    """
    Base immutable domain event.

    A DomainEvent represents a factual occurrence within the
    AfriTech platform. It records *what happened*, not *what to do*.

    A DomainEvent defines:
    - a stable event type identifier
    - an opaque, structured payload describing the fact

    It does NOT:
    - trigger behavior
    - contain timestamps or IDs
    - publish itself
    - reference infrastructure
    - encode workflows or side effects

    Event transport, persistence, and delivery are handled
    outside core.
    """

    event_type: str
    payload: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )

    # ------------------------------------------------------------------
    # Post-init normalization (deep immutability guarantee)
    # ------------------------------------------------------------------

    def __post_init__(self) -> None:
        """
        Ensure payload is deeply immutable, even if a mutable
        mapping is provided by the caller.
        """
        object.__setattr__(
            self,
            "payload",
            MappingProxyType(dict(self.payload)),
        )
