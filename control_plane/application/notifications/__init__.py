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
from .models import Channel, ChannelTarget, TemplateRef, RenderedMessage, NotificationPlan
from .protocols import TemplateRepository, TemplateBinder, ChannelRouter
from .binder import DefaultTemplateBinder
from .emitter import NotificationEmitter

__all__ = [
    "Channel", "ChannelTarget", "TemplateRef", "RenderedMessage", "NotificationPlan",
    "TemplateRepository", "TemplateBinder", "ChannelRouter",
    "DefaultTemplateBinder",
    "NotificationEmitter",
]