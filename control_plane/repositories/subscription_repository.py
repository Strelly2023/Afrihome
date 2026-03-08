from typing import Iterable, Optional, Protocol

from control_plane.governance.subscriptions.subscription import (
    Subscription,  # adjust path if needed
)
from core.typing import TenantId


class SubscriptionRepository(Protocol):
    """
    Tenant subscription snapshot access.
    """

    def snapshot_for(self, tenant_id: TenantId) -> Optional[Subscription]: ...

    """
    Subscription repository.

    Notes
    -----
    - Many products enforce at most one ACTIVE/TRIALING subscription per tenant.
    - Implementations may add uniqueness constraints accordingly.
    """

    def get_active_for_tenant(self, tenant_id: TenantId) -> Optional[Subscription]: ...
    def list_for_tenant(
        self, tenant_id: TenantId, *, limit: int = 20, offset: int = 0
    ) -> Iterable[Subscription]: ...
    def save(self, sub: Subscription) -> None: ...
