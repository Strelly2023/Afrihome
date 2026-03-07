"""
AfriHome Control Plane — Governance · Subscriptions (Phase 1.6)

Pure, deterministic models:
- Subscription aggregate (immutable transitions; no billing/infra)
- Entitlement graph (derived from a Plan + optional overrides)

This ties tenants → plans → entitlements in a constitution-safe way.
"""
from .subscription import Subscription, SubscriptionStatus, PlanChangePolicy
from .entitlement import Entitlement, EntitlementSource
from .entitlement_graph import EntitlementGraph, build_entitlements_from_plan, apply_entitlement_overrides

__all__ = [
    "Subscription",
    "SubscriptionStatus",
    "PlanChangePolicy",
    "Entitlement",
    "EntitlementSource",
    "EntitlementGraph",
    "build_entitlements_from_plan",
    "apply_entitlement_overrides",
]