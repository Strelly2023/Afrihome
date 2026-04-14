from __future__ import annotations

"""
AfriTech Core Events â€” Consent Domain Events (GA-Sealed)

This module defines immutable domain events related to consent within
the AfriTech platform.

Consent events represent *factual state changes or evaluations* of
consent. They do NOT evaluate legality, enforce access, or trigger
side effects.

PURPOSE:
- Declare the canonical event language for consent facts
- Enable deterministic audit and replay
- Decouple consent facts from enforcement and infrastructure

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
# Consent Evaluated Event
# ============================================================================

@dataclass(frozen=True, slots=True)
class ConsentEvaluated(DomainEvent):
    """
    Event emitted when consent is evaluated.

    This event records the *fact* that consent was evaluated for a
    subject and scope at a point in time, along with the resulting state.

    It does NOT:
    - grant or revoke consent
    - enforce access
    - interpret legal frameworks
    """

    consent_id: str
    subject_id: str
    scope: str
    allowed: bool
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )

    def __init__(
        self,
        *,
        consent_id: str,
        subject_id: str,
        scope: str,
        allowed: bool,
        metadata: Mapping[str, Any] | None = None,
    ):
        payload = {
            "consent_id": consent_id,
            "subject_id": subject_id,
            "scope": scope,
            "allowed": allowed,
            "metadata": dict(metadata) if metadata else {},
        }

        super().__init__(
            event_type=EventType.CONSENT_EVALUATED,
            payload=payload,
        )

        # Enforce deep immutability of metadata
        object.__setattr__(
            self,
            "metadata",
            MappingProxyType(payload["metadata"]),
        )


# ============================================================================
# Consent Granted Event
# ============================================================================

@dataclass(frozen=True, slots=True)
class ConsentGranted(DomainEvent):
    """
    Event emitted when consent is granted.

    This event records the factual occurrence that consent was granted
    for a subject under a specific consent identifier and scope.

    It does NOT:
    - evaluate legality
    - enforce downstream behavior
    """

    consent_id: str
    subject_id: str
    scope: str
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )

    def __init__(
        self,
        *,
        consent_id: str,
        subject_id: str,
        scope: str,
        metadata: Mapping[str, Any] | None = None,
    ):
        payload = {
            "consent_id": consent_id,
            "subject_id": subject_id,
            "scope": scope,
            "metadata": dict(metadata) if metadata else {},
        }

        super().__init__(
            event_type=EventType.CONSENT_GRANTED,
            payload=payload,
        )

        object.__setattr__(
            self,
            "metadata",
            MappingProxyType(payload["metadata"]),
        )


# ============================================================================
# Consent Revoked Event
# ============================================================================

@dataclass(frozen=True, slots=True)
class ConsentRevoked(DomainEvent):
    """
    Event emitted when consent is revoked.

    This event records the factual occurrence that previously granted
    consent was revoked.

    It does NOT:
    - enforce blocking
    - trigger compensation
    - evaluate policy or governance
    """

    consent_id: str
    subject_id: str
    scope: str
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )

    def __init__(
        self,
        *,
        consent_id: str,
        subject_id: str,
        scope: str,
        metadata: Mapping[str, Any] | None = None,
    ):
        payload = {
            "consent_id": consent_id,
            "subject_id": subject_id,
            "scope": scope,
            "metadata": dict(metadata) if metadata else {},
        }

        super().__init__(
            event_type=EventType.CONSENT_REVOKED,
            payload=payload,
        )

        object.__setattr__(
            self,
            "metadata",
            MappingProxyType(payload["metadata"]),
        )
