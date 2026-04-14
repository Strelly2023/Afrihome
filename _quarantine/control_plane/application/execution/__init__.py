#control_plane.application.execution.__init__.py
"""
AfriHome Control Plane — Application/Execution
PHASE: 3.1 (Orchestration only)
IO: NONE | Threads/async: NONE | Deterministic: YES

Exports:
- Header constants
- ActorKind, Actor
- ExecutionFrame
- build_request_context, new_execution_context
- resolve_tenant_context
- map_headers_to_actor
- FeatureSnapshotProvider, get_feature_snapshot
- open_execution_frame (single entrypoint)
"""
from .constants import (
    HDR_REQUEST_ID, HDR_CORRELATION_ID, HDR_CAUSATION_ID,
    HDR_TENANT_ID, HDR_TENANT_SLUG,
    HDR_ACTOR_KIND, HDR_USER_ID, HDR_ROLES, HDR_PRINCIPAL,
)
from .models import ActorKind, Actor, ExecutionFrame
from .context_factory import build_request_context, new_execution_context
from .tenant_resolution import resolve_tenant_context
from .actor_resolution import map_headers_to_actor
from .feature_snapshot import FeatureSnapshotProvider, get_feature_snapshot
from .factory import open_execution_frame

__all__ = [
    # constants
    "HDR_REQUEST_ID", "HDR_CORRELATION_ID", "HDR_CAUSATION_ID",
    "HDR_TENANT_ID", "HDR_TENANT_SLUG",
    "HDR_ACTOR_KIND", "HDR_USER_ID", "HDR_ROLES", "HDR_PRINCIPAL",
    # models
    "ActorKind", "Actor", "ExecutionFrame",
    # orchestration steps
    "build_request_context", "new_execution_context",
    "resolve_tenant_context",
    "map_headers_to_actor",
    "FeatureSnapshotProvider", "get_feature_snapshot",
    # entrypoint
    "open_execution_frame",
]