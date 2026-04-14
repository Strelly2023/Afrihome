from dataclasses import dataclass
from typing import Tuple, Optional
import re

from core.errors import InvariantViolationError
from core.typing import TenantId, UserId

from control_plane.governance.notifications.template import Channel, normalize_template_key
from control_plane.governance.features.flag_rule import ActorKind


# Event key grammar ("platform.tenant.created", "domain.booking.confirmed")
#_EVENT_KEY_RE = re.compile(r"^[a-z][a-z0-9]*(?:[._-][a-z0-9]+)*$")
_EVENT_KEY_RE = re.compile(r'^[a-z][a-z0-9]*(?:[._-][a-z0-9]+)*$')


def normalize_event_key(key: str) -> str:
    if not isinstance(key, str):
        raise InvariantViolationError("event key must be a string")
    k = key.strip().lower()
    if not _EVENT_KEY_RE.match(k):
        raise InvariantViolationError(f"Invalid event key: {key!r}")
    return k


@dataclass(frozen=True, slots=True)
class NotificationRule:
    """
    Immutable notification routing rule (pure governance).

    Fields
    ------
    rule_id        : unique identifier for audit/debug
    priority       : non-negative; lower number = higher precedence
    enabled        : on/off switch
    template_key   : which template to use (normalized)

    match_events   : Tuple[str, ...] event keys this rule applies to
    tenant_slugs   : optional whitelist
    tenant_ids     : optional whitelist
    user_ids       : optional whitelist
    actor_kinds    : optional whitelist

    channels       : Tuple[Channel, ...] to send through (must be subset of template.channels)

    Throttling metadata (governance only; application/infra enforce later):
    max_per_window : Optional[int] number of notifications allowed
    window_ms      : Optional[int] size of the window (e.g., 3600000 for 1h)

    Methods (pure helpers)
    ----------------------
    - matches(...) → bool   : whether target & event match this rule
    - select_channels(allowed_from_template) → Tuple[Channel,...] intersection
    """
    rule_id: str
    priority: int
    enabled: bool
    template_key: str

    match_events: Tuple[str, ...]
    tenant_slugs: Tuple[str, ...] = ()
    tenant_ids: Tuple[TenantId, ...] = ()
    user_ids: Tuple[UserId, ...] = ()
    actor_kinds: Tuple[ActorKind, ...] = ()

    channels: Tuple[Channel, ...] = ()

    max_per_window: Optional[int] = None
    window_ms: Optional[int] = None

    description: str = ""

    def __post_init__(self) -> None:
        if not self.rule_id or not isinstance(self.rule_id, str):
            raise InvariantViolationError("rule_id must be a non-empty string")

        p = int(self.priority)
        if p < 0:
            raise InvariantViolationError("priority must be non-negative")
        object.__setattr__(self, "priority", p)

        tk = normalize_template_key(self.template_key)
        object.__setattr__(self, "template_key", tk)

        events = tuple(normalize_event_key(e) for e in self.match_events)
        if not events:
            raise InvariantViolationError("match_events cannot be empty")
        object.__setattr__(self, "match_events", events)

        ch = tuple(self.channels)
        if not ch:
            raise InvariantViolationError("channels cannot be empty")
        object.__setattr__(self, "channels", ch)

        if self.max_per_window is not None:
            m = int(self.max_per_window)
            if m < 0:
                raise InvariantViolationError("max_per_window must be >= 0")
            object.__setattr__(self, "max_per_window", m)

        if self.window_ms is not None:
            w = int(self.window_ms)
            if w <= 0:
                raise InvariantViolationError("window_ms must be > 0")
            object.__setattr__(self, "window_ms", w)

    # ---------- Pure helpers (no IO) ----------

    def matches(
        self,
        *,
        event_key: str,
        tenant_slug: Optional[str],
        tenant_id: Optional[TenantId],
        user_id: Optional[UserId],
        actor_kind: ActorKind,
    ) -> bool:
        e = normalize_event_key(event_key)
        if e not in self.match_events or not self.enabled:
            return False

        if self.tenant_slugs:
            if tenant_slug is None or tenant_slug not in self.tenant_slugs:
                return False

        if self.tenant_ids:
            if tenant_id is None or tenant_id not in self.tenant_ids:
                return False

        if self.user_ids:
            if user_id is None or user_id not in self.user_ids:
                return False

        if self.actor_kinds:
            if actor_kind not in self.actor_kinds:
                return False

        return True

    def select_channels(self, allowed_from_template: Tuple[Channel, ...]) -> Tuple[Channel, ...]:
        allowed = set(allowed_from_template)
        # Return only channels permitted both by the template and by this rule
        inter = tuple(ch for ch in self.channels if ch in allowed)
        if not inter:
            # Governance safeguard: ensure rule cannot force disallowed channel
            # Application layer can decide to skip or use template default behavior
            return ()
        return inter