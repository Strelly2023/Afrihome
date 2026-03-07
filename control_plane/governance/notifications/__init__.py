"""
AfriHome Control Plane — Governance · Notifications (Phase 1.8)

Pure, deterministic governance models for notifications:
- NotificationTemplate : immutable, channel-aware templates with placeholder validation
- NotificationRule     : immutable routing rule with deterministic matching

No services, no infrastructure here. The application layer will:
- choose a template + rule,
- build a context,
- render (in a pure renderer),
- enqueue delivery via outbox & infra adapters.

Key grammar is aligned with other governance keys (lowercase, dot/underscore/dash separated).
"""

from .template import NotificationTemplate, Channel, normalize_template_key
from .rule import NotificationRule, normalize_event_key

__all__ = [
    "Channel",
    "normalize_template_key",
    "NotificationTemplate",
    "normalize_event_key",
    "NotificationRule",
]