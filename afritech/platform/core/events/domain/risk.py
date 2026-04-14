from __future__ import annotations

"""
AfriTech Core Events â€” Risk Domain Events (GA-Sealed)
"""

from dataclasses import dataclass, field
from typing import Mapping, Any
from types import MappingProxyType

from afritech.platform.core.events.base import DomainEvent
from afritech.platform.core.events.types import EventType


@dataclass(frozen=True, slots=True)
class RiskEvaluated(DomainEvent):
    """
    Event emitted when a risk score is evaluated.
    """

    subject_id: str
    risk_level: str
    score: int
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )

    def __init__(
        self,
        *,
        subject_id: str,
        risk_level: str,
        score: int,
        metadata: Mapping[str, Any] | None = None,
    ):
        payload = {
            "subject_id": subject_id,
            "risk_level": risk_level,
            "score": score,
            "metadata": dict(metadata) if metadata else {},
        }

        super().__init__(
            event_type=EventType.RISK_EVALUATED,
            payload=payload,
        )

        object.__setattr__(self, "metadata", MappingProxyType(payload["metadata"]))
