from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping, Protocol

from control_plane.application.entitlements.models import (
    EntitlementDecision,
    QuotaDecision,
    QuotaExceededError,
)
from control_plane.application.entitlements.protocols import (
    EntitlementProvider,  # (optional) used only by EntitlementCheckService
    QuotaPolicyProvider,
    UsageReader,
    WindowCalculator,
)
from control_plane.application.execution.models import ExecutionFrame
from control_plane.governance.entitlements import Entitlement, EntitlementSet
from control_plane.governance.plans.plan import Plan
from control_plane.governance.subscriptions.subscription import Subscription
from core.errors import ValidationError
from core.kernel.invariants import assert_not_none

# ──────────────────────────────────────────────────────────────────────────────
# Local protocol façades for derivation (keep here if you don’t already have them)
# ──────────────────────────────────────────────────────────────────────────────


class PlanRepository(Protocol):
    def get(self, plan_key: str) -> Plan: ...
    def get_default(self) -> Plan: ...


class SubscriptionRepository(Protocol):
    def get_active(self, tenant_id) -> Subscription | None: ...


class FeatureOverridesProvider(Protocol):
    """
    Provide entitlement overrides for a tenant from feature flags/rules.
    Return a normalized mapping: key -> Entitlement
    """

    def entitlement_overrides_for(self, tenant_id) -> Mapping[str, Entitlement]: ...


# ──────────────────────────────────────────────────────────────────────────────
# A) Derivation: compute EntitlementSet for a tenant (plan + overrides)
# ──────────────────────────────────────────────────────────────────────────────


@dataclass(frozen=True, slots=True)
class EntitlementsService:
    """
    Derives a deterministic EntitlementSet for a tenant:

      1) Choose effective Plan (from Subscription or default)
      2) Convert Plan features -> base Entitlements
      3) Overlay feature/subscription overrides deterministically

    Pure orchestration: protocols only, no infra/ORM.
    """

    plan_repo: PlanRepository
    subscription_repo: SubscriptionRepository
    feature_overrides: FeatureOverridesProvider

    def derive_for_tenant(self, tenant_id) -> EntitlementSet:
        assert_not_none(tenant_id, "tenant_id")

        sub: Subscription | None = self.subscription_repo.get_active(tenant_id)
        base_plan: Plan = (
            self.plan_repo.get(sub.plan_key) if sub is not None else self.plan_repo.get_default()
        )

        base_items: dict[str, Entitlement] = self._from_plan(base_plan)
        ent_set = EntitlementSet(base_items)

        overrides = self._load_overrides(tenant_id, sub)
        return ent_set.merge_overrides(overrides)

    def derive_for_frame(self, frame: ExecutionFrame) -> EntitlementSet:
        assert_not_none(frame, "frame")
        return self.derive_for_tenant(frame.tenant_id)

    # ---- internal pure helpers ----

    def _from_plan(self, plan: Plan) -> dict[str, Entitlement]:
        assert_not_none(plan, "plan")
        items: dict[str, Entitlement] = {}
        # Adjust attributes to your Plan/PlanFeature dataclasses
        for pf in getattr(plan, "features", ()):
            key = (pf.key or "").strip().lower()
            if not key:
                raise ValidationError("plan feature key must be a non-empty string")
            limit = getattr(pf, "limit", None)
            items[key] = Entitlement(key=key, limit=limit, is_unlimited=(limit is None))
        return items

    def _load_overrides(self, tenant_id, sub: Subscription | None) -> Iterable[Entitlement]:
        # If Subscription carries explicit overrides, you can fold them in here before/after features.
        overrides_map = self.feature_overrides.entitlement_overrides_for(tenant_id) or {}
        return overrides_map.values()


# ──────────────────────────────────────────────────────────────────────────────
# B) (Optional) Check service against a provider (legacy/provider-based pattern)
# ──────────────────────────────────────────────────────────────────────────────


@dataclass(frozen=True, slots=True)
class EntitlementCheckService:
    """
    Orchestrates entitlement checks against a provider.
    Pure: calls EntitlementProvider (protocol), returns immutable decisions.
    """

    entitlements: EntitlementProvider

    def check(self, frame: ExecutionFrame, entitlement_key: str) -> EntitlementDecision:
        assert_not_none(frame, "frame")
        assert_not_none(entitlement_key, "entitlement_key")
        key = entitlement_key.strip()
        if not key:
            raise ValidationError("entitlement_key must be a non-empty string")

        allowed = self.entitlements.has(frame.tenant_id, key)
        reason = (
            "allow: plan/derived entitlement present" if allowed else "deny: entitlement missing"
        )
        return EntitlementDecision(key=key, allowed=allowed, reason=reason)

    def require(self, frame: ExecutionFrame, entitlement_key: str) -> None:
        decision = self.check(frame, entitlement_key)
        if decision.allowed:
            return
        raise ValidationError(decision.reason)


# ──────────────────────────────────────────────────────────────────────────────
# C) Quota enforcement (unchanged API)
# ──────────────────────────────────────────────────────────────────────────────


@dataclass(frozen=True, slots=True)
class QuotaService:
    """
    Quota enforcement:

      1) Get policy via QuotaPolicyProvider
      2) Compute window via WindowCalculator
      3) Read usage via UsageReader
      4) Compare and return QuotaDecision; `require()` raises on exceed

    Pure: protocol calls only, no infra.
    """

    policies: QuotaPolicyProvider
    usage: UsageReader
    windows: WindowCalculator

    def enforce(self, frame: ExecutionFrame, quota_key: str) -> QuotaDecision:
        assert_not_none(frame, "frame")
        assert_not_none(quota_key, "quota_key")
        qk = quota_key.strip()
        if not qk:
            raise ValidationError("quota_key must be a non-empty string")

        policy = self.policies.policy_for(frame.tenant_id, qk)
        limit = int(policy.limit)

        # Provide consistent window context even if blocked
        wid, ws, we = self.windows.compute(
            now_ms=int(frame.ctx.now()),
            window=str(policy.window),
        )

        if limit <= 0:
            return QuotaDecision(
                quota_key=qk,
                allowed=False,
                used=0,
                limit=limit,
                remaining=0,
                window_id=wid,
                window_start_ms=ws,
                window_end_ms=we,
                reason="deny: quota limit is non-positive (policy)",
            )

        used = int(self.usage.used(frame.tenant_id, qk, wid))
        remaining = max(0, limit - used)
        allowed = used < limit
        reason = "allow: under quota" if allowed else "deny: quota exhausted"

        return QuotaDecision(
            quota_key=qk,
            allowed=allowed,
            used=used,
            limit=limit,
            remaining=remaining,
            window_id=wid,
            window_start_ms=ws,
            window_end_ms=we,
            reason=reason,
        )

    def require(self, frame: ExecutionFrame, quota_key: str) -> None:
        decision = self.enforce(frame, quota_key)
        if decision.allowed:
            return
        raise QuotaExceededError(decision.reason)
