from dataclasses import dataclass, replace
from typing import Dict, Iterable, Tuple

from core.typing import UnixMillis
from control_plane.governance.plans.plan import Plan
from control_plane.governance.subscriptions.entitlement import Entitlement, EntitlementSource


@dataclass(frozen=True, slots=True)
class EntitlementGraph:
    """
    Immutable set of effective entitlements for a (plan, version).
    Tenant-scoping and persistence are handled by upper layers.
    """
    plan_key: str
    plan_version: int
    generated_ms: UnixMillis
    items: Tuple[Entitlement, ...]


def build_entitlements_from_plan(*, plan: Plan, now_ms: UnixMillis) -> EntitlementGraph:
    """
    Deterministically derive entitlements from a Plan.
    """
    items = tuple(
        Entitlement(
            feature_key=pf.feature_key,
            enabled=pf.enabled_default,
            quota_limit=pf.quota_limit,
            overage_policy=pf.overage_policy,
            source=EntitlementSource.PLAN_DEFAULT,
            note="from_plan",
        )
        for pf in plan.features
    )
    return EntitlementGraph(
        plan_key=plan.key,
        plan_version=plan.version,
        generated_ms=now_ms,
        items=items,
    )


def apply_entitlement_overrides(
    *,
    graph: EntitlementGraph,
    overrides: Iterable[Entitlement],
    now_ms: UnixMillis,
) -> EntitlementGraph:
    """
    Apply a set of per-subscription overrides on top of a plan-derived graph,
    returning a new graph (pure). Overrides must declare source=OVERRIDE.
    """
    idx: Dict[str, Entitlement] = {e.feature_key: e for e in graph.items}
    for ov in overrides:
        if ov.source is not EntitlementSource.OVERRIDE:
            # guardrail: don't allow mixing sources
            continue
        idx[ov.feature_key] = ov
    # Keep deterministic order by feature_key
    items = tuple(idx[k] for k in sorted(idx.keys()))
    return EntitlementGraph(
        plan_key=graph.plan_key,
        plan_version=graph.plan_version,
        generated_ms=now_ms,
        items=items,
    )