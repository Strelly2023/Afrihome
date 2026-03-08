from dataclasses import dataclass

from control_plane.application.execution.models import ExecutionFrame
from core.errors import AuthorizationError, ValidationError
from core.events import DomainEvent, EventEnvelope, EventHeaders
from core.kernel.invariants import assert_not_none
from core.typing import UnixMillis

from .models import (
    Boundary,
    BoundaryDecision,
    ChangeKind,
    ChangePlanDecision,
    PlanRef,
    SubscriptionSnapshot,
    SubscriptionStatus,
)
from .protocols import PlanCatalog, SubscriptionReader, TransitionPolicy


@dataclass(frozen=True, slots=True)
class SubscriptionService:
    """
    Orchestrates subscription lifecycle changes and boundary enforcement.
    - No IO: reads state via SubscriptionReader (protocol), never writes.
    - Classifies upgrade/downgrade via PlanCatalog.
    - Applies TransitionPolicy (pure) to decide effectivity/proration hints.
    - Emits pure DomainEvent/EventEnvelope for outbox (later phases).
    """

    reader: SubscriptionReader
    catalog: PlanCatalog
    policy: TransitionPolicy
    change_event_type: str = "subscription.plan.change.requested"

    # ---------- Plan change orchestration ----------

    def propose_change(self, frame: ExecutionFrame, target_plan_id: str) -> ChangePlanDecision:
        assert_not_none(frame, "frame")
        if not target_plan_id or not target_plan_id.strip():
            raise ValidationError("target_plan_id must be a non-empty string")
        to_plan: PlanRef = self.catalog.plan_ref(target_plan_id.strip())

        snap: SubscriptionSnapshot = self.reader.snapshot_for(frame.tenant_id)
        kind = self._classify_change(snap.current_plan, to_plan)

        # Policy decides allow/deny + when to apply
        allowed, reason, effective_at_period_boundary, proration = self.policy.evaluate(
            snapshot=snap, to_plan=to_plan, kind=kind
        )

        effective_ms: UnixMillis
        if effective_at_period_boundary:
            if snap.period_end_ms is None:
                # No known boundary → default to "now" but keep reason explicit
                effective_ms = frame.ctx.now()
                reason = f"{reason}; period_end unknown → default now"
            else:
                effective_ms = snap.period_end_ms
        else:
            effective_ms = frame.ctx.now()

        return ChangePlanDecision(
            allowed=bool(allowed),
            reason=reason,
            kind=kind,
            from_plan=snap.current_plan,
            to_plan=to_plan,
            effective_ms=effective_ms,
            effective_at_period_boundary=bool(effective_at_period_boundary),
            proration_recommended=bool(proration),
        )

    def build_change_event(
        self, frame: ExecutionFrame, decision: ChangePlanDecision
    ) -> EventEnvelope:
        """
        Produce a pure EventEnvelope describing the requested plan change.
        No IO; outbox persistence/dispatch happens in later phases.
        """
        assert_not_none(frame, "frame")
        assert_not_none(decision, "decision")

        evt = DomainEvent(
            event_id=frame.ctx.uuid_provider.new_event_id(),
            event_type=self.change_event_type,
            payload={
                "tenant_id": str(frame.tenant_id),
                "kind": decision.kind.name,
                "from_plan": decision.from_plan.plan_id,
                "to_plan": decision.to_plan.plan_id,
                "allowed": decision.allowed,
                "effective_ms": int(decision.effective_ms),
                "effective_at_period_boundary": decision.effective_at_period_boundary,
                "proration_recommended": decision.proration_recommended,
                "reason": decision.reason,
            },
        )
        headers = EventHeaders(
            correlation_id=frame.correlation_id,
            causation_id=frame.causation_id,
            timestamp_ms=frame.timestamp_ms,
            tenant_id=frame.tenant_id,
        )
        return EventEnvelope.create(evt, headers)

    # ---------- Enforcement boundaries ----------

    def enforce_boundary(self, frame: ExecutionFrame, boundary: Boundary) -> BoundaryDecision:
        """
        Deterministic guardrails that gate actions based on subscription status.
        Returns a decision; call-sites may also use `require_boundary(...)`.
        """
        assert_not_none(frame, "frame")
        snap: SubscriptionSnapshot = self.reader.snapshot_for(frame.tenant_id)

        if boundary is Boundary.REQUIRES_ACTIVE:
            if (
                snap.status is SubscriptionStatus.ACTIVE
                or snap.status is SubscriptionStatus.TRIALING
            ):
                return BoundaryDecision(True, boundary, "allow: subscription is active or trialing")
            return BoundaryDecision(
                False, boundary, f"deny: subscription status={snap.status.name}"
            )

        if boundary is Boundary.BILLING_WRITE_ALLOWED:
            # Conservative: disallow writes on CANCELED; allow on ACTIVE/TRIALING; allow on PAST_DUE but mark reason
            if snap.status is SubscriptionStatus.CANCELED:
                return BoundaryDecision(False, boundary, "deny: subscription canceled")
            if snap.status is SubscriptionStatus.PAST_DUE:
                return BoundaryDecision(True, boundary, "warn: past_due — allow write with caution")
            return BoundaryDecision(True, boundary, "allow: billing write permitted")

        # Unknown boundary → default deny (safe)
        return BoundaryDecision(False, boundary, "deny: unknown boundary")

    def require_boundary(self, frame: ExecutionFrame, boundary: Boundary) -> None:
        dec = self.enforce_boundary(frame, boundary)
        if dec.allowed:
            return
        raise AuthorizationError(dec.reason)

    # ---------- Internals ----------

    @staticmethod
    def _classify_change(current: PlanRef, target: PlanRef) -> ChangeKind:
        if target.tier > current.tier:
            return ChangeKind.UPGRADE
        if target.tier < current.tier:
            return ChangeKind.DOWNGRADE
        return ChangeKind.LATERAL
