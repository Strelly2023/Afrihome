from __future__ import annotations

"""
AfriTech Core Events â€” Authorization Domain Events (GA-Sealed)

This module defines immutable domain events related to authorization
outcomes within the AfriTech platform.

Authorization events represent *factual outcomes* of the decision
system. They record that a decision was made, without encoding
decision logic, enforcement, or side effects.

PURPOSE:
- Declare the canonical event language for authorization facts
- Enable deterministic audit and replay
- Decouple decision facts from enforcement and infrastructure

RULES:
- Pure data ONLY
- NO execution
- NO IO
- NO time generation
- NO enforcement or orchestration
- MUST be immutable

Any change requires an ADR.
"""

from dataclasses import dataclass, field
from typing import Mapping, Any
from types import MappingProxyType

from afritech.platform.core.events.base import DomainEvent
from afritech.platform.core.events.types import EventType


# ============================================================================
# Authorization Decided Event (Factual Outcome)
# ============================================================================

@dataclass(frozen=True, slots=True)
class AuthorizationDecided(DomainEvent):
    """
    Event emitted when an authorization decision is made.

    This event records the *fact* that the decision system produced
    an authorization outcome for a subject, action, and resource.

    It does NOT:
    - perform authorization
    - enforce access
    - interpret policies or governance
    - trigger side effects

    It is a factual record only.
    """

    allowed: bool
    subject_id: str
    action: str
    resource: str
    reasons: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )

    def __init__(
        self,
        *,
        allowed: bool,
        subject_id: str,
        action: str,
        resource: str,
        reasons: Mapping[str, Any] | None = None,
    ):
        """
        Create an immutable authorization decision event.

        The meaning of `allowed` and the structure of `reasons`
        are defined elsewhere (e.g. core/decision and audit layers).
        """
        payload = {
            "allowed": allowed,
            "subject_id": subject_id,
            "action": action,
            "resource": resource,
            "reasons": dict(reasons) if reasons else {},
        }

        super().__init__(
            event_type=EventType.AUTHORIZATION_DECIDED,
            payload=payload,
        )

        # Enforce deep immutability of reasons at the event surface
        object.__setattr__(
            self,
            "reasons",
            MappingProxyType(payload["reasons"]),
        )
