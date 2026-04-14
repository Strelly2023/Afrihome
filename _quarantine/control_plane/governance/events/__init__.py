"""
AfriHome Governance — Platform Events (Pure Contract)
No IO • No ORM • Deterministic
"""
from .event_type import EventType
from .platform_event import PlatformEvent
from .event_envelope import PlatformEnvelope

__all__ = ["EventType", "PlatformEvent", "PlatformEnvelope"]