from __future__ import annotations

"""
AfriTech Core Events â€” Audit Domain Events (GA-Sealed)

This module defines immutable domain events related to audit recording
within the AfriTech platform.

Audit events represent *facts* that an auditable record was created.
They do NOT perform logging, persistence, enforcement, or interpretation.

PURPOSE:
- Declare the canonical event language for audit facts
- Enable deterministic audit reconstruction and compliance replay
- Decouple audit recording from infrastructure and storage

RULES:
- Pure data ONLY
- NO execution
- NO IO
- NO time generation
- NO logging or persistence
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
# Audit Recorded Event (Factual Record)
# ============================================================================

@dataclass(frozen=True, slots=True)
class AuditRecorded(DomainEvent):
    """
    Event emitted when an auditable record is created.

    This event records the *fact* that an audit record exists
    for a particular action or decision.

    It does NOT:
    - persist audit data
    - log to files or monitoring systems
    - interpret decision logic
    - enforce compliance
    """

    record_id: str
    subject_id: str
    action: str
    resource: str
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )

    def __init__(
        self,
        *,
        record_id: str,
        subject_id: str,
        action: str,
        resource: str,
        metadata: Mapping[str, Any] | None = None,
    ):
        """
        Create an immutable audit-recorded event.

        All identifiers and metadata are supplied externally.
        Core does not generate IDs, timestamps, or persistence.
        """
        payload = {
            "record_id": record_id,
            "subject_id": subject_id,
            "action": action,
            "resource": resource,
            "metadata": dict(metadata) if metadata else {},
        }

        super().__init__(
            event_type=EventType.AUDIT_RECORDED,
            payload=payload,
        )

        # Enforce deep immutability of metadata at the event surface
        object.__setattr__(
            self,
            "metadata",
            MappingProxyType(payload["metadata"]),
        )
