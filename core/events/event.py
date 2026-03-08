"""
GA Enterprise Core — Immutable Domain Event
-------------------------------------------

LAYER: L2
Dependencies:
- core.typing
- core.kernel.invariants

Rules:
- Immutable
- No time access
- No ID generation
- No mutation
"""

from dataclasses import dataclass
from typing import Any, Mapping

from core.kernel.invariants import assert_not_none
from core.typing import EventId


@dataclass(frozen=True, slots=True)
class DomainEvent:
    """
    Immutable domain event.

    event_id must be injected by caller.
    payload must be deterministic and JSON‑serialisable.
    """

    event_id: EventId
    event_type: str
    payload: Mapping[str, Any]

    def __post_init__(self) -> None:
        assert_not_none(self.event_id, "event_id")
        assert_not_none(self.event_type, "event_type")
        assert_not_none(self.payload, "payload")

    def to_dict(self) -> dict[str, Any]:
        """
        Deterministic conversion to a JSON‑safe mapping.
        """
        return {
            "event_id": str(self.event_id),
            "event_type": self.event_type,
            "payload": dict(self.payload),
        }
