"""
GA Repository Protocol — RBAC State
-----------------------------------

Layer: Repositories (ports only; no IO)
Deterministic: YES
IO/ORM: NO

Purpose
-------
Tenant-scoped storage boundary for the complete RBAC state snapshot
(roles registry + user->roles assignments).

Notes
-----
• Implementations live in control_plane/infrastructure/* and must not leak infra types upward.
• Methods must be deterministic for identical inputs.
• Saving the same state twice must be idempotent.
"""

from typing import Optional, Protocol, runtime_checkable

from control_plane.governance.rbac.rbac_state import RBACState
from control_plane.governance.tenants.tenant_id import TenantId


@runtime_checkable
class RbacStateRepository(Protocol):
    """
    RBACState snapshot repository.

    Scope
    -----
    - Persist/Load an immutable RBACState for a given scope (typically tenant).
    - Coarse-grained by design; assignments & role definitions are versioned inside RBACState.
    """

    def get_for_tenant(self, tenant_id: TenantId) -> Optional[RBACState]: ...

    def save_for_tenant(self, tenant_id: TenantId, state: RBACState) -> None:
        ...
        # Idempotent "upsert": same state written again is a no-op.

    # Back-compat alias


RBACStateRepository = RbacStateRepository
