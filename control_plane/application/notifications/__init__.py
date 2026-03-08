"""
AfriHome Control Plane — Application/Notifications
PHASE: 3.10 (Orchestration only)
IO: NONE | Threads/async: NONE | Deterministic: YES

Exports:
- Channel, ChannelTarget, TemplateRef, RenderedMessage, NotificationPlan
- TemplateRepository, TemplateBinder, ChannelRouter
- DefaultTemplateBinder
- NotificationEmitter
"""

from control_plane.governance.notifications.models import (
    Channel,
    ChannelTarget,
    NotificationPlan,
    RenderedMessage,
    TemplateRef,
)

from .binder import DefaultTemplateBinder
from .emitter import NotificationEmitter
from .protocols import ChannelRouter, TemplateBinder, TemplateRepository

__all__ = [
    "Channel",
    "ChannelTarget",
    "TemplateRef",
    "RenderedMessage",
    "NotificationPlan",
    "TemplateRepository",
    "TemplateBinder",
    "ChannelRouter",
    "DefaultTemplateBinder",
    "NotificationEmitter",
]
