from dataclasses import dataclass
from core.kernel.invariants import assert_not_none
from core.errors import ValidationError
from control_plane.application.execution.models import ExecutionFrame
from .models import EntitlementDecision, QuotaDecision, QuotaExceededError
from .protocols import EntitlementProvider, QuotaPolicyProvider, UsageReader, WindowCalculator

# =========================
# Entitlements (plan)
# =========================

@dataclass(frozen=True, slots=True)
class EntitlementsService:
    """
    Orchestrates plan entitlement checks.
    Pure: calls a protocol, returns an immutable decision.
    """
    entitlements: EntitlementProvider

    def check(self, frame: ExecutionFrame, entitlement_key: str) -> EntitlementDecision:
        assert_not_none(frame, "frame")
        assert_not_none(entitlement_key, "entitlement_key")
        key = entitlement_key.strip()
        if not key:
            raise ValidationError("entitlement_key must be a non-empty string")
        allowed = self.entitlements.has(frame.tenant_id, key)
        reason = "allow: plan entitlement present" if allowed else "deny: plan entitlement missing"
        return EntitlementDecision(key=key, allowed=allowed, reason=reason)

# =========================
# Quota enforcement
# =========================

@dataclass(frozen=True, slots=True)
class QuotaService:
    """
    Orchestrates quota enforcement:
      1) Get policy (limit, window kind) via QuotaPolicyProvider
      2) Compute window id/bounds with WindowCalculator (pure)
      3) Read usage count via UsageReader (pure interface)
      4) Compare and return immutable decision; optional exception guard
    No IO/ORM here—only protocols and core invariants.
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

        # 1) Policy
        policy = self.policies.policy_for(frame.tenant_id, qk)
        limit = int(policy.limit)
        if limit <= 0:
            # A zero/negative limit means "blocked by policy"
            wid, ws, we = self.windows.compute(now_ms=int(frame.ctx.now()), window=str(policy.window))
            return QuotaDecision(
                quota_key=qk, allowed=False,
                used=0, limit=limit, remaining=0,
                window_id=wid, window_start_ms=ws, window_end_ms=we,
                reason="deny: quota limit is non-positive (policy)",
            )

        # 2) Window
        wid, ws, we = self.windows.compute(now_ms=int(frame.ctx.now()), window=str(policy.window))

        # 3) Usage
        used = int(self.usage.used(frame.tenant_id, qk, wid))
        remaining = max(0, limit - used)

        # 4) Decision
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
        """
        Exception-based guard for call sites that prefer raising on exceed.
        """
        decision = self.enforce(frame, quota_key)
        if decision.allowed:
            return
        raise QuotaExceededError(decision.reason)