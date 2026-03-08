"""
AfriHome Control Plane — Governance · Plans (Phase 1.5)

Pure models:
- PlanFeature        : per-feature entitlement (enabled/quota/etc.)
- TierMeta           : tier metadata (code, billing cadence, price metadata)
- Plan               : immutable plan aggregate (versioned, features, tier)

No I/O here. Application layer will compose Plans with Subscriptions/Entitlements.
"""

from .plan import Plan, normalize_plan_key
from .plan_feature import OveragePolicy, PlanFeature
from .tier import BillingCycle, TierMeta, normalize_tier_code

__all__ = [
    "PlanFeature",
    "OveragePolicy",
    "TierMeta",
    "BillingCycle",
    "normalize_tier_code",
    "Plan",
    "normalize_plan_key",
]
