from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Mapping, Optional, Tuple


class Channel(Enum):
    EMAIL = auto()
    SMS = auto()
    WEBHOOK = auto()


@dataclass(frozen=True, slots=True)
class TemplateRef:
    """
    Opaque reference to a template (id + optional language).
    The repository protocol owns semantics; app only carries refs.
    """

    template_id: str
    language: Optional[str] = None


@dataclass(frozen=True, slots=True)
class RenderedMessage:
    """
    Pure, immutable render result.
    """

    subject: Optional[str]
    body_text: Optional[str]
    body_html: Optional[str]
    variables: Mapping[str, Any]


@dataclass(frozen=True, slots=True)
class ChannelTarget:
    """
    Where to send the message (no deliverability here).
    """

    channel: Channel
    address: str  # email, phone, or webhook URL
    metadata: Mapping[str, Any] = ()  # channel-specific tags (e.g., categories)


@dataclass(frozen=True, slots=True)
class NotificationPlan:
    """
    Immutable orchestration plan for one outbound message to N targets.
    """

    template: TemplateRef
    rendered: RenderedMessage
    targets: Tuple[ChannelTarget, ...]
    attributes: Mapping[str, Any] = ()  # extra context for auditing (e.g., category, key)
