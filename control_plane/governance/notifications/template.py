import re
from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional, Tuple

from core.errors import InvariantViolationError

# Reuse a consistent grammar with features/plans: "a", "a.b", "a-b_c"
# _KEY_RE = re.compile(r"^[a-z][a-z0-9]*(?:[._-][a-z0-9]+)*$")
_KEY_RE = re.compile(r"^[a-z][a-z0-9]*(?:[._-][a-z0-9]+)*$")


def normalize_template_key(key: str) -> str:
    if not isinstance(key, str):
        raise InvariantViolationError("template key must be a string")
    k = key.strip().lower()
    if not _KEY_RE.match(k):
        raise InvariantViolationError(f"Invalid template key: {key!r}")
    return k


class Channel(Enum):
    EMAIL = auto()
    SMS = auto()
    WEBHOOK = auto()


@dataclass(frozen=True, slots=True)
class NotificationTemplate:
    """
    Immutable, channel-aware notification template (governance model).

    Fields
    ------
    template_key     : canonical key (normalized)
    version          : >= 1 (bump on breaking changes)
    channels         : allowed channels for this template
    subject_template : optional subject (EMAIL only)
    body_template    : body template (for EMAIL/SMS; webhook uses payload_template)
    payload_template : optional JSON-ish string for webhooks (pure text here)
    placeholders     : required placeholders, e.g. ("tenant_name","link")

    Rules
    -----
    - No I/O; rendering is a separate pure concern in application layer.
    - We validate that declared placeholders appear at least once in the template(s).
    - Channel presence implies corresponding template pieces must be provided:
        EMAIL   -> body_template required; subject_template optional
        SMS     -> body_template required
        WEBHOOK -> payload_template required
    """

    template_key: str
    version: int
    channels: Tuple[Channel, ...]

    body_template: Optional[str] = None
    subject_template: Optional[str] = None  # email-only
    payload_template: Optional[str] = None  # webhook-only

    placeholders: Tuple[str, ...] = ()
    description: str = ""
    locale: Optional[str] = None  # e.g., "en-US", "fr-FR"

    def __post_init__(self) -> None:
        k = normalize_template_key(self.template_key)
        object.__setattr__(self, "template_key", k)

        v = int(self.version)
        if v < 1:
            raise InvariantViolationError("template version must be >= 1")
        object.__setattr__(self, "version", v)

        # Validate required content per channel
        ch = tuple(self.channels)
        if not ch:
            raise InvariantViolationError("at least one channel must be specified")
        object.__setattr__(self, "channels", ch)

        if Channel.EMAIL in ch or Channel.SMS in ch:
            if not self.body_template or not self.body_template.strip():
                raise InvariantViolationError("body_template is required for EMAIL/SMS")
        if Channel.WEBHOOK in ch:
            if not self.payload_template or not self.payload_template.strip():
                raise InvariantViolationError("payload_template is required for WEBHOOK")

        # Placeholders: each must be a non-empty, lowercase key
        ph = tuple(self.placeholders)
        for p in ph:
            if not isinstance(p, str) or not p.strip() or p != p.strip().lower():
                raise InvariantViolationError(
                    f"invalid placeholder {p!r}; must be lowercase non-empty string"
                )
        object.__setattr__(self, "placeholders", ph)

        # Ensure placeholders appear somewhere in provided templates (governance safeguard)
        if ph:
            haystacks = []
            if self.body_template:
                haystacks.append(self.body_template)
            if self.subject_template:
                haystacks.append(self.subject_template)
            if self.payload_template:
                haystacks.append(self.payload_template)
            missing = tuple(p for p in ph if not any(("{{" + p + "}}" in h) for h in haystacks))
            if missing:
                raise InvariantViolationError(f"placeholders not found in templates: {missing}")
