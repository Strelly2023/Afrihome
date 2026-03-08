from typing import Optional, Protocol, Tuple

from control_plane.governance.identity.user import User  # adjust path if needed
from core.typing import TenantId, UserId


class IdentityRepository(Protocol):
    """
    Users/identity read contract (no IO here).
    """

    def get_user(self, tenant_id: TenantId, user_id: UserId) -> Optional[User]: ...
    def find_user_by_email(self, tenant_id: TenantId, email: str) -> Optional[User]: ...
    def list_users(
        self, tenant_id: TenantId, *, limit: int = 100, offset: int = 0
    ) -> Tuple[User, ...]: ...
