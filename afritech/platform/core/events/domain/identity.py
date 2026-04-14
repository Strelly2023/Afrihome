from __future__ import annotations

"""
AfriTech Core Events â€” Identity Domain Events (GA-Sealed)
"""

from dataclasses import dataclass
from afritech.platform.core.events.base import DomainEvent
from afritech.platform.core.events.types import EventType


@dataclass(frozen=True, slots=True)
class IdentityCreated(DomainEvent):
    identity_id: str
    identity_type: str  # user, service, device

    def __init__(self, *, identity_id: str, identity_type: str):
        super().__init__(
            event_type=EventType.IDENTITY_CREATED,
            payload={
                "identity_id": identity_id,
                "identity_type": identity_type,
            },
        )


@dataclass(frozen=True, slots=True)
class IdentityDeactivated(DomainEvent):
    identity_id: str
    reason: str

    def __init__(self, *, identity_id: str, reason: str):
        super().__init__(
            event_type=EventType.IDENTITY_DEACTIVATED,
            payload={
                "identity_id": identity_id,
                "reason": reason,
            },
        )
