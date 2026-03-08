# control_plane/application/execution/factory.py
from typing import Dict, Mapping

from core.identity.uuid import UUIDProvider
from core.kernel.invariants import assert_not_none
from core.tenancy import TenantResolver
from core.time.clock import Clock

from .actor_resolution import map_headers_to_actor
from .context_factory import build_request_context, new_execution_context
from .feature_snapshot import FeatureSnapshotProvider, get_feature_snapshot
from .models import ExecutionFrame
from .tenant_resolution import resolve_tenant_context


def _normalize_headers(headers: Mapping[str, str]) -> Dict[str, str]:
    return {
        str(k).strip().lower(): str(v).strip()
        for k, v in headers.items()
        if isinstance(k, str) and isinstance(v, str)
    }


def open_execution_frame(
    *,
    headers: Mapping[str, str],
    clock: Clock,
    uuid: UUIDProvider,
    tenant_resolver: TenantResolver,
    feature_provider: FeatureSnapshotProvider,
) -> ExecutionFrame:
    """
    Deterministic orchestration for a single inbound call.
      1) Build RequestContext (IDs/time injected) -> ExecutionContext
      2) Resolve Tenant (ID > Slug) via pure resolver
      3) Map headers -> Actor (no RBAC)
      4) Attach feature snapshot (opaque) via provider protocol
      5) Return immutable ExecutionFrame
    """
    assert_not_none(headers, "headers")
    assert_not_none(clock, "clock")
    assert_not_none(uuid, "uuid")
    assert_not_none(tenant_resolver, "tenant_resolver")
    assert_not_none(feature_provider, "feature_provider")

    H = _normalize_headers(headers)

    # 1) Build core contexts
    rc = build_request_context(H, clock, uuid)
    ec = new_execution_context(rc, clock, uuid)

    # 2) Tenant resolution
    tctx = resolve_tenant_context(H, tenant_resolver)

    # 3) Actor mapping
    actor = map_headers_to_actor(H)

    # 4) Feature snapshot injection
    features = get_feature_snapshot(feature_provider, tctx.tenant_id, ec.now())

    # 5) Assemble immutable frame (includes core ExecutionContext)
    return ExecutionFrame(
        ctx=ec,
        request_id=rc.request_id,
        correlation_id=rc.correlation_id,
        causation_id=rc.causation_id,
        timestamp_ms=rc.timestamp_ms,
        tenant_id=tctx.tenant_id,
        tenant_slug=tctx.slug,
        actor=actor,
        feature_snapshot=features,
        headers=H,
    )
