from dataclasses import dataclass
from typing import Mapping, Any
from core.kernel.invariants import assert_not_none
from .event_type import EventType

@dataclass(frozen=True, slots=True)
class PlatformEvent:
    """
    Type + payload (opaque mapping).
    """
    type: EventType
    payload: Mapping[str, Any]

    def __post_init__(self) -> None:
        assert_not_none(self.type, "type")
        assert_not_none(self.payload, "payload")