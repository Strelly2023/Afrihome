import re
from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional, Tuple
from urllib.parse import urlparse

from core.errors import InvariantViolationError

# Canonical “key” grammar (consistent with features/plans/etc.)
# _KEY_RE = re.compile(r"^[a-z][a-z0-9]*(?:[._-][a-z0-9]+)*$")
_KEY_RE = re.compile(r"^[a-z][a-z0-9]*(?:[._-][a-z0-9]+)*$")


def normalize_provider_key(key: str) -> str:
    if not isinstance(key, str):
        raise InvariantViolationError("provider key must be a string")
    k = key.strip().lower()
    if not _KEY_RE.match(k):
        raise InvariantViolationError(f"Invalid provider key: {key!r}")
    return k


def normalize_namespace_key(key: str) -> str:
    """
    Namespace for events or logical grouping under a provider.
    e.g., "provider.stripe", "provider.sendgrid", "provider.twilio"
    """
    if not isinstance(key, str):
        raise InvariantViolationError("namespace must be a string")
    k = key.strip().lower()
    if not _KEY_RE.match(k):
        raise InvariantViolationError(f"Invalid namespace: {key!r}")
    return k


def _validate_https_url(optional_url: Optional[str]) -> Optional[str]:
    if optional_url is None:
        return None
    url = optional_url.strip()
    if not url:
        return None
    parsed = urlparse(url)
    # Governance safeguard: prefer HTTPS scheme
    if parsed.scheme not in ("https",):
        raise InvariantViolationError("base_url must use https scheme")
    if not parsed.netloc:
        raise InvariantViolationError("base_url must include host")
    return url


@dataclass(frozen=True, slots=True)
class ProviderConfig:
    """
    Immutable provider registry entry (governance-only).

    Fields
    ------
    provider_key    : canonical key ("stripe", "sendgrid", "twilio-sms")
    kind            : ProviderKind classification (governance signal)
    display_name    : human label (for admin UI)
    enabled         : on/off switch (governance control)
    base_url        : optional https base URL for admin/docs/etc. (no IO)
    event_namespace : canonical namespace for provider-originating events
    tags            : optional governance tags, as (key,value) tuples

    Notes
    -----
    - No secrets here (use opaque refs in app/infra layers).
    - No HTTP/SDK calls here (governance-only).
    """

    provider_key: str
    kind: "ProviderKind"
    display_name: str
    enabled: bool
    base_url: Optional[str] = None
    event_namespace: Optional[str] = None
    tags: Tuple[Tuple[str, str], ...] = ()

    def __post_init__(self) -> None:
        k = normalize_provider_key(self.provider_key)
        object.__setattr__(self, "provider_key", k)

        if not isinstance(self.display_name, str) or not self.display_name.strip():
            raise InvariantViolationError("display_name cannot be empty")
        object.__setattr__(self, "display_name", self.display_name.strip())

        bu = _validate_https_url(self.base_url)
        object.__setattr__(self, "base_url", bu)

        if self.event_namespace is not None:
            ns = normalize_namespace_key(self.event_namespace)
            object.__setattr__(self, "event_namespace", ns)

        # tags: ensure shape Tuple[Tuple[str,str],...]
        if any((not isinstance(a, str) or not isinstance(b, str)) for a, b in self.tags):
            raise InvariantViolationError("tags must be Tuple[Tuple[str,str], ...]")


class ProviderKind(Enum):
    EMAIL = auto()
    SMS = auto()
    WEBHOOK = auto()
    PAYMENTS = auto()
    STORAGE = auto()
    ANALYTICS = auto()
    CUSTOM = auto()
