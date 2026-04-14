from typing import Protocol, Optional
from control_plane.governance.events.event_type import EventType

class EventTypeRegistry(Protocol):
    """
    Pure registry for platform event types (prevents string drift).
    """
    def get(self, name: str) -> Optional[EventType]: ...
    def exists(self, name: str) -> bool: ...
