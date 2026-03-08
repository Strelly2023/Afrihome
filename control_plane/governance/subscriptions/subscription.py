from dataclasses import dataclass, replace
from enum import Enum, auto
from typing import Optional

from control_plane.governance.plans.plan import normalize_plan_key
from core.errors import InvariantViolationError
from core.typing import TenantId, UnixMillis


class SubscriptionStatus(Enum):
    """
    Subscription lifecycle (governance view).
    Billing/payment states are handled later in application/infra.
    """

    TRIALING = auto()
    ACTIVE = auto()
    SUSPENDED = auto()
    CANCELED = auto()


class PlanChangePolicy(Enum):
    """When changing plan, apply immediately or at the next period boundary."""

    IMMEDIATE = auto()
    NEXT_PERIOD = auto()


@dataclass(frozen=True, slots=True)
class Subscription:
    """
    Immutable subscription aggregate (pure, deterministic).

    Fields (governance)
    -------------------
    tenant_id: TenantId
    plan_key: str                 # canonical (normalized)
    plan_version: int             # governance version pin
    status: SubscriptionStatus
    started_ms: UnixMillis
    current_period_start_ms: UnixMillis
    current_period_end_ms: UnixMillis
    trial_end_ms: Optional[UnixMillis]
    cancel_at_period_end: bool
    canceled_at_ms: Optional[UnixMillis]
    suspended_ms: Optional[UnixMillis]
    updated_ms: UnixMillis

    Scheduled plan change (governance)
    ----------------------------------
    next_plan_key: Optional[str]
    next_plan_version: Optional[int]

    Notes
    -----
    - No billing/proration here.
    - No I/O; all transitions are pure (return new instances).
    """

    tenant_id: TenantId

    plan_key: str
    plan_version: int

    status: SubscriptionStatus

    started_ms: UnixMillis
    current_period_start_ms: UnixMillis
    current_period_end_ms: UnixMillis

    trial_end_ms: Optional[UnixMillis] = None
    cancel_at_period_end: bool = False
    canceled_at_ms: Optional[UnixMillis] = None
    suspended_ms: Optional[UnixMillis] = None

    updated_ms: UnixMillis = 0

    # optional scheduled change
    next_plan_key: Optional[str] = None
    next_plan_version: Optional[int] = None

    def __post_init__(self) -> None:
        k = normalize_plan_key(self.plan_key)
        object.__setattr__(self, "plan_key", k)

        v = int(self.plan_version)
        if v < 1:
            raise InvariantViolationError("plan_version must be >= 1")
        object.__setattr__(self, "plan_version", v)

        # Period window
        if int(self.current_period_end_ms) <= int(self.current_period_start_ms):
            raise InvariantViolationError("current_period_end_ms must be > current_period_start_ms")

        # Timestamps sanity
        for name in (
            "started_ms",
            "current_period_start_ms",
            "current_period_end_ms",
            "updated_ms",
        ):
            val = getattr(self, name)
            if int(val) < 0:
                raise InvariantViolationError(f"{name} must be non-negative")

        if self.trial_end_ms is not None and int(self.trial_end_ms) < int(self.started_ms):
            raise InvariantViolationError("trial_end_ms cannot be earlier than started_ms")

        if self.next_plan_key is not None:
            nk = normalize_plan_key(self.next_plan_key)
            object.__setattr__(self, "next_plan_key", nk)
        if self.next_plan_version is not None:
            nv = int(self.next_plan_version)
            if nv < 1:
                raise InvariantViolationError("next_plan_version must be >= 1")
            object.__setattr__(self, "next_plan_version", nv)

    # ----------- Factories -----------

    @staticmethod
    def start(
        *,
        tenant_id: TenantId,
        plan_key: str,
        plan_version: int,
        started_ms: UnixMillis,
        period_start_ms: UnixMillis,
        period_end_ms: UnixMillis,
        trial_end_ms: Optional[UnixMillis] = None,
    ) -> "Subscription":
        """
        Start a new subscription. Status is TRIALING if trial_end_ms > now, else ACTIVE.
        """
        status = (
            SubscriptionStatus.TRIALING
            if (trial_end_ms is not None and int(trial_end_ms) > int(started_ms))
            else SubscriptionStatus.ACTIVE
        )
        return Subscription(
            tenant_id=tenant_id,
            plan_key=plan_key,
            plan_version=plan_version,
            status=status,
            started_ms=started_ms,
            current_period_start_ms=period_start_ms,
            current_period_end_ms=period_end_ms,
            trial_end_ms=trial_end_ms,
            cancel_at_period_end=False,
            canceled_at_ms=None,
            suspended_ms=None,
            updated_ms=started_ms,
        )

    # ----------- Helpers -----------

    def is_active(self) -> bool:
        return self.status in (SubscriptionStatus.TRIALING, SubscriptionStatus.ACTIVE)

    # ----------- Transitions (pure) -----------

    def suspend(self, now_ms: UnixMillis) -> "Subscription":
        if self.status is SubscriptionStatus.CANCELED:
            raise InvariantViolationError("Cannot suspend a canceled subscription")
        if self.status is SubscriptionStatus.SUSPENDED:
            return replace(self, updated_ms=now_ms)  # idempotent
        return replace(
            self, status=SubscriptionStatus.SUSPENDED, suspended_ms=now_ms, updated_ms=now_ms
        )

    def resume(self, now_ms: UnixMillis) -> "Subscription":
        if self.status is SubscriptionStatus.CANCELED:
            raise InvariantViolationError("Cannot resume a canceled subscription")
        if self.status in (SubscriptionStatus.ACTIVE, SubscriptionStatus.TRIALING):
            return replace(self, updated_ms=now_ms)  # idempotent
        # Resume -> ACTIVE; trial has no meaning after suspension
        return replace(self, status=SubscriptionStatus.ACTIVE, suspended_ms=None, updated_ms=now_ms)

    def cancel_now(self, now_ms: UnixMillis) -> "Subscription":
        if self.status is SubscriptionStatus.CANCELED:
            return replace(self, updated_ms=now_ms)  # idempotent
        return replace(
            self,
            status=SubscriptionStatus.CANCELED,
            canceled_at_ms=now_ms,
            cancel_at_period_end=False,
            updated_ms=now_ms,
        )

    def cancel_at_end(self, now_ms: UnixMillis) -> "Subscription":
        if self.status is SubscriptionStatus.CANCELED:
            return replace(self, updated_ms=now_ms)  # idempotent
        return replace(self, cancel_at_period_end=True, updated_ms=now_ms)

    def uncancel(self, now_ms: UnixMillis) -> "Subscription":
        if self.status is SubscriptionStatus.CANCELED:
            raise InvariantViolationError("Cannot uncancel a canceled subscription")
        if not self.cancel_at_period_end:
            return replace(self, updated_ms=now_ms)  # idempotent
        return replace(self, cancel_at_period_end=False, updated_ms=now_ms)

    def schedule_plan_change(
        self, *, next_plan_key: str, next_plan_version: int, now_ms: UnixMillis
    ) -> "Subscription":
        if self.status is SubscriptionStatus.CANCELED:
            raise InvariantViolationError("Cannot schedule plan change on canceled subscription")
        return replace(
            self,
            next_plan_key=next_plan_key,
            next_plan_version=next_plan_version,
            updated_ms=now_ms,
        )

    def apply_scheduled_plan_change(self, now_ms: UnixMillis) -> "Subscription":
        if self.next_plan_key is None or self.next_plan_version is None:
            return replace(self, updated_ms=now_ms)  # no-op
        return replace(
            self,
            plan_key=self.next_plan_key,
            plan_version=self.next_plan_version,
            next_plan_key=None,
            next_plan_version=None,
            updated_ms=now_ms,
        )

    def change_plan(
        self,
        *,
        new_plan_key: str,
        new_plan_version: int,
        policy: PlanChangePolicy,
        now_ms: UnixMillis,
    ) -> "Subscription":
        if policy is PlanChangePolicy.NEXT_PERIOD:
            return self.schedule_plan_change(
                next_plan_key=new_plan_key, next_plan_version=new_plan_version, now_ms=now_ms
            )
        # IMMEDIATE
        return replace(
            self,
            plan_key=new_plan_key,
            plan_version=new_plan_version,
            next_plan_key=None,
            next_plan_version=None,
            updated_ms=now_ms,
        )

    def renew_period(
        self, *, new_start_ms: UnixMillis, new_end_ms: UnixMillis, now_ms: UnixMillis
    ) -> "Subscription":
        """
        Start a new period. If cancel_at_period_end is True, the subscription cancels at renewal.
        If a plan change was scheduled, it is applied at renewal boundary.
        """
        if int(new_end_ms) <= int(new_start_ms):
            raise InvariantViolationError("new period end must be > new period start")

        s = self
        # Apply scheduled plan change at boundary
        if s.next_plan_key is not None and s.next_plan_version is not None:
            s = s.apply_scheduled_plan_change(now_ms=now_ms)

        # Apply cancel-at-end at boundary
        if s.cancel_at_period_end:
            return replace(
                s,
                status=SubscriptionStatus.CANCELED,
                canceled_at_ms=now_ms,
                cancel_at_period_end=False,  # reset
                current_period_start_ms=new_start_ms,
                current_period_end_ms=new_end_ms,
                updated_ms=now_ms,
            )

        # Normal renewal
        # Trialing does not continue across periods; remain ACTIVE if previously trialing and trial ended
        new_status = s.status
        if (
            new_status is SubscriptionStatus.TRIALING
            and (s.trial_end_ms is not None)
            and int(s.trial_end_ms) <= int(new_start_ms)
        ):
            new_status = SubscriptionStatus.ACTIVE

        return replace(
            s,
            status=new_status,
            current_period_start_ms=new_start_ms,
            current_period_end_ms=new_end_ms,
            updated_ms=now_ms,
        )
