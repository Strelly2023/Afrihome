from __future__ import annotations

"""
AfriTech Core Events â€” Policy Domain Events (GA-Sealed)
"""

from dataclasses import dataclass, field
from typing import Mapping, Any
from types import MappingProxyType

from afritech.platform.core.events.base import DomainEvent
from afritech.platform.core.events.types import EventType


@dataclass(frozen=True, slots=True)
class PolicyEvaluated(DomainEvent):
    """
    Event emitted when a policy is evaluated.
    """

    policy_id: str
    subject_id: str
    allowed: bool
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )

    def __init__(
        self,
        *,
        policy_id: str,
        subject_id: str,
        allowed: bool,
        metadata: Mapping[str, Any] | None = None,
    ):
        payload = {
            "policy_id": policy_id,
            "subject_id": subject_id,
            "allowed": allowed,
            "metadata": dict(metadata) if metadata else {},
        }

        super().__init__(
            event_type=EventType.POLICY_EVALUATED,
            payload=payload,
        )

        object.__setattr__(self, "metadata", MappingProxyType(payload["metadata"]))
