from typing import Dict, Optional, Protocol

from core.rbac.roles import Role  # pure role model (already in core)
from core.typing import RoleName


class RoleRepository(Protocol):
    """
    RBAC roles catalog per application (policy layer will assemble tenant-scoped policies).
    """

    def get(self, name: RoleName) -> Optional[Role]: ...
    def all_roles(self) -> Dict[str, Role]: ...
