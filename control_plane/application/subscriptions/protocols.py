from typing import Protocol, runtime_checkable
from core.typing import TenantId
from .models import SubscriptionSnapshot, PlanRef, ChangeKind

@runtime_checkable
class SubscriptionReader(Protocol):
    """
    Pure read contract for current subscription state.
    Bound to infra later (Phase 5) via repositories/adapters.
    """
    def snapshot_for(self, tenant_id: TenantId) -> SubscriptionSnapshot: ...

@runtime_checkable
class PlanCatalog(Protocol):
    """
    Pure plan catalog contract (no IO in app layer).
    Provides rank/tier to classify change kind deterministically.
    """
    def plan_ref(self, plan_id: str) -> PlanRef: ...

@runtime_checkable
class TransitionPolicy(Protocol):
    """
    Pure policy defining whether a change is allowed and how it should be applied.
    Return (allowed, reason, effective_at_period_boundary, proration_recommended).
    """
    def evaluate(self, *, snapshot: SubscriptionSnapshot, to_plan: PlanRef, kind: ChangeKind) -> tuple[bool, str, bool, bool]: ...