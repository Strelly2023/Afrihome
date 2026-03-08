"""
AfriHome Governance — Platform Events (Pure Contract)
No IO • No ORM • Deterministic
"""

from .event_envelope import PlatformEnvelope
from .event_type import EventType
from .platform_event import PlatformEvent

__all__ = ["EventType", "PlatformEvent", "PlatformEnvelope"]
