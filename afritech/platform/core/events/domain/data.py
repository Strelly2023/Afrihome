from __future__ import annotations

"""
AfriTech Core Events â€” Data Domain Events (GA-Sealed)
"""

from dataclasses import dataclass
from afritech.platform.core.events.base import DomainEvent
from afritech.platform.core.events.types import EventType


@dataclass(frozen=True, slots=True)
class DataCreated(DomainEvent):
    data_id: str
    data_type: str

    def __init__(self, *, data_id: str, data_type: str):
        super().__init__(
            event_type=EventType.DATA_CREATED,
            payload={
                "data_id": data_id,
                "data_type": data_type,
            },
        )


@dataclass(frozen=True, slots=True)
class DataDeleted(DomainEvent):
    data_id: str
    reason: str

    def __init__(self, *, data_id: str, reason: str):
        super().__init__(
            event_type=EventType.DATA_DELETED,
            payload={
                "data_id": data_id,
                "reason": reason,
            },
        )
