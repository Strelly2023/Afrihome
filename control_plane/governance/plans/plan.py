import re
from dataclasses import dataclass, replace
from typing import Dict, Tuple

from core.errors import InvariantViolationError
from core.typing import UnixMillis

from .plan_feature import PlanFeature
from .tier import TierMeta

# _PLAN_KEY_RE = re.compile(r"^[a-z][a-z0-9]*(?:[._-][a-z0-9]+)*$")
_PLAN_KEY_RE = re.compile(r"^[a-z][a-z0-9]*(?:[._-][a-z0-9]+)*$")


def normalize_plan_key(key: str) -> str:
    if not isinstance(key, str):
        raise InvariantViolationError("Plan key must be a string")
    k = key.strip().lower()
    if not _PLAN_KEY_RE.match(k):
        raise InvariantViolationError(f"Invalid plan key: {key!r}")
    return k


@dataclass(frozen=True, slots=True)
class Plan:
    """
    Immutable plan aggregate (governance only).

    Fields
    ------
    key        : canonical plan key (e.g., "core.pro", "enterprise.eu")
    name       : display name
    version    : integer version (bumped on breaking changes)
    tier       : TierMeta metadata
    features   : tuple of PlanFeature
    active     : governance activation (not billing/contract state)
    created_ms : injected
    updated_ms : injected

    Transitions are pure (return new instances).
    No persistence, no billing math, no adapters here.
    """

    key: str
    name: str
    version: int
    tier: TierMeta
    features: Tuple[PlanFeature, ...]
    active: bool
    created_ms: UnixMillis
    updated_ms: UnixMillis

    def __post_init__(self) -> None:
        k = normalize_plan_key(self.key)
        object.__setattr__(self, "key", k)

        n = (self.name or "").strip()
        if not n:
            raise InvariantViolationError("Plan name cannot be empty")
        if len(n) > 160:
            raise InvariantViolationError("Plan name too long")
        object.__setattr__(self, "name", n)

        v = int(self.version)
        if v < 1:
            raise InvariantViolationError("Plan version must be >= 1")
        object.__setattr__(self, "version", v)

        # Validate uniqueness of feature keys within the tuple
        keys = [pf.feature_key for pf in self.features]
        if len(keys) != len(set(keys)):
            raise InvariantViolationError("Duplicate feature_key in plan.features is not allowed")

        cm = int(self.created_ms)
        um = int(self.updated_ms)
        if cm < 0 or um < 0:
            raise InvariantViolationError("Timestamps must be non-negative")
        if um < cm:
            raise InvariantViolationError("updated_ms cannot be earlier than created_ms")

    # ---------- Accessors ----------

    def features_map(self) -> Dict[str, PlanFeature]:
        """Build a deterministic copy of features by key."""
        return {pf.feature_key: pf for pf in self.features}

    def get_feature(self, feature_key: str) -> PlanFeature | None:
        return self.features_map().get(feature_key)

    # ---------- Transitions (pure) ----------

    def activate(self, now_ms: UnixMillis) -> "Plan":
        return replace(self, active=True, updated_ms=now_ms)

    def suspend(self, now_ms: UnixMillis) -> "Plan":
        return replace(self, active=False, updated_ms=now_ms)

    def bump_version(self, new_version: int, now_ms: UnixMillis) -> "Plan":
        v = int(new_version)
        if v <= self.version:
            raise InvariantViolationError("new_version must be greater than current version")
        return replace(self, version=v, updated_ms=now_ms)

    def rename(self, name: str, now_ms: UnixMillis) -> "Plan":
        n = (name or "").strip()
        if not n:
            raise InvariantViolationError("Plan name cannot be empty")
        return replace(self, name=n, updated_ms=now_ms)

    def with_feature(self, feature: PlanFeature, now_ms: UnixMillis) -> "Plan":
        fm = self.features_map()
        fm[feature.feature_key] = feature
        new_features = tuple(fm[k] for k in sorted(fm.keys()))
        return replace(self, features=new_features, updated_ms=now_ms)

    def without_feature(self, feature_key: str, now_ms: UnixMillis) -> "Plan":
        fm = self.features_map()
        if feature_key not in fm:
            # idempotent removal: keep updated_ms to reflect attempted change
            return replace(self, updated_ms=now_ms)
        del fm[feature_key]
        new_features = tuple(fm[k] for k in sorted(fm.keys()))
        return replace(self, features=new_features, updated_ms=now_ms)

    def with_tier(self, tier: TierMeta, now_ms: UnixMillis) -> "Plan":
        return replace(self, tier=tier, updated_ms=now_ms)
