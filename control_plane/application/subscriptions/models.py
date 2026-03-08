from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional

from core.typing import UnixMillis


class SubscriptionStatus(Enum):
    """Pure subscription lifecycle states (no IO)."""

    TRIALING = auto()
    ACTIVE = auto()
    PAST_DUE = auto()
    CANCELED = auto()


@dataclass(frozen=True, slots=True)
class PlanRef:
    """Opaque reference to a plan in the catalog; 'tier' ranks relative value."""

    plan_id: str
    tier: int  # higher = richer plan


@dataclass(frozen=True, slots=True)
class SubscriptionSnapshot:
    """Immutable snapshot of the tenant's current subscription."""

    status: SubscriptionStatus
    current_plan: PlanRef
    started_ms: UnixMillis
    period_end_ms: Optional[UnixMillis] = None
    cancel_at_period_end: bool = False


class ChangeKind(Enum):
    """Classification of the requested plan change."""

    UPGRADE = auto()
    DOWNGRADE = auto()
    LATERAL = auto()


@dataclass(frozen=True, slots=True)
class ChangePlanDecision:
    """Immutable orchestration outcome for a plan change request."""

    allowed: bool
    reason: str
    kind: ChangeKind
    from_plan: PlanRef
    to_plan: PlanRef
    effective_ms: UnixMillis  # when change should take effect
    effective_at_period_boundary: bool  # True if apply at period end (common for downgrades)
    proration_recommended: bool  # **hint** only; actual billing handled later


class Boundary(Enum):
    """Named enforcement boundaries"""

    REQUIRES_ACTIVE = auto()
    BILLING_WRITE_ALLOWED = auto()


@dataclass(frozen=True, slots=True)
class BoundaryDecision:
    allowed: bool
    boundary: Boundary
    reason: str
