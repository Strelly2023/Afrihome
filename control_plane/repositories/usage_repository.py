# from core.typing.primitives import UserId
from typing import Iterable, Optional, Protocol

# from core.typing import TenantId, UserId
from control_plane.governance.identity import User
from core.typing import TenantId, UserId


class UsageRepository(Protocol):
    """
    Provides usage counters and aggregations through pure interfaces.
    Actual storage/aggregation is handled by infra/worker layers.
    """

    def used(self, tenant_id: TenantId, key: str, window_id: str) -> int: ...

    """
    User repository contract (tenant-scoped identities).

    Notes
    -----
    - Email uniqueness is typically enforced per-tenant (or globally if required by your product rules).
    """

    def get_by_id(self, user_id: UserId) -> Optional[User]: ...
    def get_by_tenant_and_email(self, tenant_id: TenantId, email: str) -> Optional[User]: ...
    def list_by_tenant(
        self, tenant_id: TenantId, *, limit: int = 100, offset: int = 0
    ) -> Iterable[User]: ...
    def save(self, user: User) -> None: ...
