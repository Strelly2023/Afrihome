from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional

from control_plane.governance.plans.plan_feature import OveragePolicy


class EntitlementSource(Enum):
    PLAN_DEFAULT = auto()
    OVERRIDE = auto()


@dataclass(frozen=True, slots=True)
class Entitlement:
    """
    Effective entitlement for a single feature.

    - feature_key     : canonical key
    - enabled         : True/False for this subscription
    - quota_limit     : Optional[int] (>=0) if applicable
    - overage_policy  : OveragePolicy (conceptual; app/infra enforce later)
    - source          : PLAN_DEFAULT or OVERRIDE
    - note            : Optional textual reason
    """

    feature_key: str
    enabled: bool
    source: EntitlementSource
    quota_limit: Optional[int] = None
    overage_policy: OveragePolicy = OveragePolicy.NONE
    note: str = ""
