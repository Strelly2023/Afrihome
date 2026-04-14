from __future__ import annotations

"""
AfriTech Core Events â€” Device Domain Events (GA-Sealed)
"""

from dataclasses import dataclass
from afritech.platform.core.events.base import DomainEvent
from afritech.platform.core.events.types import EventType


@dataclass(frozen=True, slots=True)
class DeviceRegistered(DomainEvent):
    device_id: str
    device_type: str

    def __init__(self, *, device_id: str, device_type: str):
        super().__init__(
            event_type=EventType.DEVICE_REGISTERED,
            payload={
                "device_id": device_id,
                "device_type": device_type,
            },
        )


@dataclass(frozen=True, slots=True)
class DeviceDecommissioned(DomainEvent):
    device_id: str
    reason: str

    def __init__(self, *, device_id: str, reason: str):
        super().__init__(
            event_type=EventType.DEVICE_DECOMMISSIONED,
            payload={
                "device_id": device_id,
                "reason": reason,
            },
        )
