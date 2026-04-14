from __future__ import annotations

"""
AfriTech Core Events â€” Notification Domain Events (GA-Sealed)
"""

from dataclasses import dataclass
from afritech.platform.core.events.base import DomainEvent
from afritech.platform.core.events.types import EventType


@dataclass(frozen=True, slots=True)
class NotificationDispatched(DomainEvent):
    notification_id: str
    channel: str

    def __init__(self, *, notification_id: str, channel: str):
        super().__init__(
            event_type=EventType.NOTIFICATION_DISPATCHED,
            payload={
                "notification_id": notification_id,
                "channel": channel,
            },
        )


@dataclass(frozen=True, slots=True)
class NotificationFailed(DomainEvent):
    notification_id: str
    reason: str

    def __init__(self, *, notification_id: str, reason: str):
        super().__init__(
            event_type=EventType.NOTIFICATION_FAILED,
            payload={
                "notification_id": notification_id,
                "reason": reason,
            },
        )
