from __future__ import annotations

from typing import Mapping, Optional, Protocol, Tuple, runtime_checkable

from control_plane.governance.entitlements import Entitlement
from control_plane.governance.plans.plan import Plan
from control_plane.governance.subscriptions.subscription import Subscription
from core.typing import TenantId

# ----------------------
# Entitlements (plan / overrides)
# ----------------------


@runtime_checkable
class EntitlementProvider(Protocol):
    """
    Pure provider for plan/derived entitlements.
    Implementations are bound later (infra/registry).
    """

    def has(self, tenant_id: TenantId, entitlement_key: str) -> bool: ...


class FeatureOverridesProvider(Protocol):
    """
    Deterministically provide entitlement overrides (key -> Entitlement) for a tenant.
    No IO here—infra implements the adapter; tests use in-memory fakes.
    """

    def entitlement_overrides_for(self, tenant_id: TenantId) -> Mapping[str, Entitlement]: ...


class PlanRepository(Protocol):
    """
    Read-only access to Plan snapshots needed for entitlement derivation.
    """

    def get(self, plan_key: str) -> Plan: ...
    def get_default(self) -> Plan: ...


class SubscriptionRepository(Protocol):
    """
    Resolve the tenant's active subscription (if any).
    """

    def get_active(self, tenant_id: TenantId) -> Optional[Subscription]: ...


# ----------------------
# Quotas
# ----------------------


class WindowKind:
    """
    Logical kinds for windowing; concrete arithmetic is provided by WindowCalculator.
    """

    FIXED_MINUTE = "fixed_minute"
    FIXED_HOUR = "fixed_hour"
    FIXED_DAY = "fixed_day"
    FIXED_MONTH = "fixed_month"


class QuotaPolicy(Protocol):
    """
    A pure, immutable policy descriptor for a quota key.
    """

    @property
    def quota_key(self) -> str: ...
    @property
    def limit(self) -> int: ...
    @property
    def window(self) -> str: ...  # one of WindowKind.*
    @property
    def attributes(self) -> Mapping[str, str] | None: ...  # optional policy tags


@runtime_checkable
class QuotaPolicyProvider(Protocol):
    """
    Returns the quota policy for a tenant + quota_key.
    Pure interface; infra binds concrete implementation later.
    """

    def policy_for(self, tenant_id: TenantId, quota_key: str) -> QuotaPolicy: ...


@runtime_checkable
class UsageReader(Protocol):
    """
    Returns current usage count for a tenant/quota/window.
    Pure interface; collection/storage handled in Phases 5–7.
    """

    def used(self, tenant_id: TenantId, quota_key: str, window_id: str) -> int: ...


@runtime_checkable
class WindowCalculator(Protocol):
    """
    Computes deterministic window identifiers and bounds.
    """

    def compute(self, *, now_ms: int, window: str) -> Tuple[str, int, int]:
        """
        Returns: (window_id, window_start_ms, window_end_ms)
        """
        ...


__all__ = [
    "EntitlementProvider",
    "FeatureOverridesProvider",
    "PlanRepository",
    "SubscriptionRepository",
    "WindowKind",
    "QuotaPolicy",
    "QuotaPolicyProvider",
    "UsageReader",
    "WindowCalculator",
]
