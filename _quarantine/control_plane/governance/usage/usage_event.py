from dataclasses import dataclass
from typing import Optional, Tuple

import re
from core.typing import UnixMillis, TenantId, UserId
from core.errors import InvariantViolationError
from control_plane.governance.features.feature_flag import normalize_feature_key
from control_plane.governance.features.flag_rule import ActorKind

# Canonical metric key grammar (same shape as feature keys)
#_METRIC_KEY_RE = re.compile(r"^[a-z][a-z0-9]*(?:[._-][a-z0-9]+)*$")
_METRIC_KEY_RE = re.compile(r'^[a-z][a-z0-9]*(?:[._-][a-z0-9]+)*$')


def normalize_metric_key(key: str) -> str:
    if not isinstance(key, str):
        raise InvariantViolationError("metric key must be a string")
    k = key.strip().lower()
    if not _METRIC_KEY_RE.match(k):
        raise InvariantViolationError(f"Invalid metric key: {key!r}")
    return k


@dataclass(frozen=True, slots=True)
class UsageEvent:
    """
    Immutable usage event (governance-only).

    - feature_key   : canonical feature (reuses feature grammar)
    - metric_key    : canonical metric name (e.g., "api.requests", "export.rows")
    - quantity      : >= 0 integer (default 1)
    - timestamp_ms  : injected event time (UnixMillis)
    - tenant_id     : TenantId (required)
    - user_id       : optional user
    - actor_kind    : USER / API_KEY / SYSTEM / OPERATOR
    - tags          : deterministic tuple of (key, value) pairs for segmentation (optional)

    Notes:
    - No I/O or id generation here.
    - Keep tags small and deterministic (sorted externally or before construction, if needed).
    """
    feature_key: str
    metric_key: str
    quantity: int
    timestamp_ms: UnixMillis
    tenant_id: TenantId
    actor_kind: ActorKind
    user_id: Optional[UserId] = None
    tags: Tuple[Tuple[str, str], ...] = ()

    def __post_init__(self) -> None:
        fk = normalize_feature_key(self.feature_key)
        mk = normalize_metric_key(self.metric_key)
        object.__setattr__(self, "feature_key", fk)
        object.__setattr__(self, "metric_key", mk)

        q = int(self.quantity)
        if q < 0:
            raise InvariantViolationError("quantity must be >= 0")
        object.__setattr__(self, "quantity", q)

        # Make sure tags are tuples of (str, str) and immutable
        if any((not isinstance(k, str) or not isinstance(v, str)) for k, v in self.tags):
            raise InvariantViolationError("tags must be Tuple[Tuple[str,str], ...]")