from __future__ import annotations

"""
AfriTech Core Events â€” Quota Domain Events (GA-Sealed)

This module defines immutable domain events related to quota usage
within the AfriTech platform.

Quota events represent factual occurrences (e.g. consumption,
exhaustion). They do NOT evaluate quota rules, enforce limits,
or trigger side effects.

PURPOSE:
- Declare the canonical event language for quota facts
- Enable deterministic audit and replay
- Decouple quota events from execution and infrastructure

RULES:
- Pure data ONLY
- NO execution
- NO IO
- NO time generation
- NO enforcement or evaluation
- MUST be immutable

Any change requires an ADR.
"""

from dataclasses import dataclass, field
from typing import Mapping, Any
from types import MappingProxyType

from afritech.platform.core.events.base import DomainEvent
from afritech.platform.core.events.types import EventType


# ============================================================================
# Quota Consumed Event
# ============================================================================

@dataclass(frozen=True, slots=True)
class QuotaConsumed(DomainEvent):
    """
    Event emitted when quota units are consumed.

    This event records the fact that a subject consumed a specific
    amount of quota under a given quota identifier.

    It does NOT:
    - decide whether the consumption was allowed
    - evaluate quota limits
    - update storage
    - trigger enforcement
    """

    quota_id: str
    subject_id: str
    amount: int

    def __init__(
        self,
        *,
        quota_id: str,
        subject_id: str,
        amount: int,
        attributes: Mapping[str, Any] | None = None,
    ):
        super().__init__(
            event_type=EventType.QUOTA_CONSUMED,
            payload={
                "quota_id": quota_id,
                "subject_id": subject_id,
                "amount": amount,
                "attributes": dict(attributes) if attributes else {},
            },
        )


# ============================================================================
# Quota Exhausted Event
# ============================================================================

@dataclass(frozen=True, slots=True)
class QuotaExhausted(DomainEvent):
    """
    Event emitted when a quota is exhausted.

    This event records the factual state that no remaining quota
    is available for a subject under a quota identifier.

    It does NOT:
    - prevent further actions
    - enforce blocking
    - evaluate policies or governance
    """

    quota_id: str
    subject_id: str

    def __init__(
        self,
        *,
        quota_id: str,
        subject_id: str,
        attributes: Mapping[str, Any] | None = None,
    ):
        super().__init__(
            event_type=EventType.QUOTA_EXHAUSTED,
            payload={
                "quota_id": quota_id,
                "subject_id": subject_id,
                "attributes": dict(attributes) if attributes else {},
            },
        )
