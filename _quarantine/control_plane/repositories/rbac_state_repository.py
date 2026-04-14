#control_plane/repositories.rbac_state_repository.py
from typing import Protocol, Optional, runtime_checkable

from control_plane.governance.rbac.rbac_state import RBACState
from core.typing import TenantId



@runtime_checkable
class RBACStateRepository(Protocol):
    """
    RBACState snapshot repository.

    Scope
    -----
    - Persist/Load an immutable RBACState for a given scope (typically tenant).
    - Coarse-grained by design; assignments & role definitions are versioned inside RBACState.
    """

    def get_for_tenant(self, tenant_id: TenantId) -> Optional[RBACState]: ...
    def save_for_tenant(self, tenant_id: TenantId, state: RBACState) -> None: ...