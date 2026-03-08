# control_plane/governance/entitlements/__init__.py
"""
GA Governance — Entitlements (pure derived domain)
--------------------------------------------------

Purpose
-------
Represents derived entitlements used across plans/subscriptions/usage/rate limiting.
This module is pure and deterministic (no IO, no ORM).

Exports
-------
- Entitlement
- EntitlementSet
- QuotaLimit
"""

from .entitlement import Entitlement
from .entitlement_set import EntitlementSet
from .quota_limit import QuotaLimit

__all__ = [
    "Entitlement",
    "EntitlementSet",
    "QuotaLimit",
]
