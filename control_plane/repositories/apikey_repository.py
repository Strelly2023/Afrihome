from typing import Optional, Protocol, Tuple

from control_plane.governance.api_keys.api_key import ApiKey
from control_plane.governance.api_keys.api_key_id import ApiKeyId
from core.typing import TenantId


class ApiKeyRepository(Protocol):
    """
    Pure contract for reading API key aggregates (no secrets).
    Infra binds storage later (DB/cache).
    """

    def get_by_id(self, tenant_id: TenantId, key_id: ApiKeyId) -> Optional[ApiKey]: ...
    def list_for_tenant(
        self, tenant_id: TenantId, *, limit: int = 100, offset: int = 0
    ) -> Tuple[ApiKey, ...]: ...
