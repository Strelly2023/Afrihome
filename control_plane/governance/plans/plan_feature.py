from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional

from control_plane.governance.features.feature_flag import normalize_feature_key
from core.errors import InvariantViolationError


class OveragePolicy(Enum):
    """
    Governance-only signal for how over-usage is *conceptually* treated.
    Application/infra will implement actual behavior later.
    """

    NONE = auto()  # no overage allowed (hard block)
    ALLOW_METERED = auto()  # allow and meter for later billing
    ALLOW_SOFT = auto()  # allow but soft-warn (no billing implied here)


@dataclass(frozen=True, slots=True)
class PlanFeature:
    """
    Pure entitlement for a single feature within a Plan/Tier.

    - feature_key         : normalized canonical key (same grammar as feature flags)
    - enabled_default     : default availability for tenants on this plan
    - quota_limit         : optional integer >= 0 (governance metadata)
    - overage_policy      : how over-usage is conceptually treated (governance)
    - description         : optional human text, not used for logic
    """

    feature_key: str
    enabled_default: bool
    quota_limit: Optional[int] = None
    overage_policy: OveragePolicy = OveragePolicy.NONE
    description: str = ""

    def __post_init__(self) -> None:
        k = normalize_feature_key(self.feature_key)
        object.__setattr__(self, "feature_key", k)

        if self.quota_limit is not None:
            q = int(self.quota_limit)
            if q < 0:
                raise InvariantViolationError("quota_limit must be >= 0 when provided")
            object.__setattr__(self, "quota_limit", q)
