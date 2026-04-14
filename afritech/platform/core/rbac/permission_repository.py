#===== ./afritech.platform.core.rbac/permission_repository.py =====
# control_plane/governance/rbac/permission_repository.py
'''

from __future__ import annotations

from typing import Protocol, Optional, Dict, runtime_checkable

from afritech.platform.core.typing import PermissionName
from afritech.platform.core.rbac.permission import PermissionDefinition


@runtime_checkable
class PermissionRepository(Protocol):
    """
    GAâ€‘v1 RBAC Permission Repository (Permission Catalog)

    PURPOSE
    -------
    Provides governanceâ€‘level PermissionDefinition objects.

    Permissions in GAâ€‘v1 are:
      - GLOBAL (not tenantâ€‘scoped)
      - STATIC (no runtime mutation)
      - IMMUTABLE once loaded

    Role composition, permission evaluation, and effective access
    decisions are handled by RBACState and Authorization services.

    RESPONSIBILITIES
    ----------------
    - Store and expose canonical PermissionDefinition objects
    - Provide readâ€‘only access to permission metadata
    - Act as the sourceâ€‘ofâ€‘truth for permission definitions

    NONâ€‘RESPONSIBILITIES
    --------------------
    - Does NOT assign permissions to roles
    - Does NOT evaluate permissions
    - Does NOT enforce authorization
    - Does NOT mutate permissions at runtime

    GAâ€‘v1 ASSUMPTIONS
    ----------------
    - Permission names are globally unique
    - Permission definitions are immutable
    - Missing permissions are expected and MUST NOT raise
    """

    # ============================================================
    # Read paths
    # ============================================================

    def get(self, name: PermissionName) -> Optional[PermissionDefinition]:
        """
        Retrieve a permission definition by canonical permission name.

        Semantics
        ---------
        - Returns PermissionDefinition if the permission exists
        - Returns None if the permission does not exist
        - MUST NOT raise for "not found"

        Guarantees
        ----------
        - Returned PermissionDefinition MUST be immutable
        - Returned instance MUST NOT expose internal mutable state

        Parameters
        ----------
        name:
            Canonical permission name
            (e.g. "invoice.read", "user.create")

        Returns
        -------
        Optional[PermissionDefinition]
        """
        ...

    def all_permissions(self) -> Dict[str, PermissionDefinition]:
        """
        Return all known permission definitions.

        Semantics
        ---------
        - Keys MUST be canonical permissionâ€‘name strings
        - Values MUST be immutable PermissionDefinition objects
        - Returned mapping MUST NOT expose internal mutable state

        Guarantees
        ----------
        - Deterministic ordering is RECOMMENDED
        - Safe to cache
        - Replayâ€‘safe

        Returns
        -------
        Dict[str, PermissionDefinition]
        """
        ...

'''
