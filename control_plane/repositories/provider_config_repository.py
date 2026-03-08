# control_plane/repositories.provider_config_repository.py
from typing import Iterable, Optional, Protocol, runtime_checkable

from control_plane.governance.integrations.provider_config import ProviderConfig


@runtime_checkable
class ProviderConfigRepository(Protocol):
    """
    Provider registry repository.
    """

    def get_by_key(self, provider_key: str) -> Optional[ProviderConfig]: ...
    def list_all(self, *, limit: int = 200, offset: int = 0) -> Iterable[ProviderConfig]: ...
    def save(self, pc: ProviderConfig) -> None: ...
