"""
AfriHome Control Plane — Application/Subscriptions
PHASE: 3.6 (Orchestration only)
IO: NONE | Threads/async: NONE | Deterministic: YES

Exports:
- SubscriptionStatus, PlanRef, SubscriptionSnapshot
- ChangeKind, ChangePlanDecision, Boundary, BoundaryDecision
- SubscriptionReader, PlanCatalog, TransitionPolicy
- SubscriptionService
"""
from .models import (
    SubscriptionStatus, PlanRef, SubscriptionSnapshot,
    ChangeKind, ChangePlanDecision,
    Boundary, BoundaryDecision,
)
from .protocols import SubscriptionReader, PlanCatalog, TransitionPolicy
from .service import SubscriptionService

__all__ = [
    "SubscriptionStatus", "PlanRef", "SubscriptionSnapshot",
    "ChangeKind", "ChangePlanDecision",
    "Boundary", "BoundaryDecision",
    "SubscriptionReader", "PlanCatalog", "TransitionPolicy",
    "SubscriptionService",
]