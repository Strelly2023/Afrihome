from __future__ import annotations

"""
AfriTech Core Events â€” Operations Domain Events (GA-Sealed)
"""

from dataclasses import dataclass
from afritech.platform.core.events.base import DomainEvent
from afritech.platform.core.events.types import EventType


@dataclass(frozen=True, slots=True)
class OperationStarted(DomainEvent):
    operation_id: str
    operation_type: str

    def __init__(self, *, operation_id: str, operation_type: str):
        super().__init__(
            event_type=EventType.OPERATION_STARTED,
            payload={
                "operation_id": operation_id,
                "operation_type": operation_type,
            },
        )


@dataclass(frozen=True, slots=True)
class OperationCompleted(DomainEvent):
    operation_id: str
    status: str

    def __init__(self, *, operation_id: str, status: str):
        super().__init__(
            event_type=EventType.OPERATION_COMPLETED,
            payload={
                "operation_id": operation_id,
                "status": status,
            },
        )
