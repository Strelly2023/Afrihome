from __future__ import annotations

"""
AfriTech Core Events â€” Tenancy Domain Events (GA-Sealed)
"""

from dataclasses import dataclass
from afritech.platform.core.events.base import DomainEvent
from afritech.platform.core.events.types import EventType


@dataclass(frozen=True, slots=True)
class TenantCreated(DomainEvent):
    tenant_id: str

    def __init__(self, *, tenant_id: str):
        super().__init__(
            event_type=EventType.TENANT_CREATED,
            payload={"tenant_id": tenant_id},
        )


@dataclass(frozen=True, slots=True)
class TenantSuspended(DomainEvent):
    tenant_id: str
    reason: str

    def __init__(self, *, tenant_id: str, reason: str):
        super().__init__(
            event_type=EventType.TENANT_SUSPENDED,
            payload={
                "tenant_id": tenant_id,
                "reason": reason,
            },
        )
