from typing import Protocol, Optional
from core.typing import TenantId
from control_plane.application.providers.models import ProviderRef, ProviderConfig  # pure app models


class ProviderRepository(Protocol):
    """
    Non-sensitive provider configuration store (no secrets).
    """
    def get(self, tenant_id: TenantId, provider: ProviderRef) -> Optional[ProviderConfig]: ...