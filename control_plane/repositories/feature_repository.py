from typing import Any, Iterable, Optional, Protocol

from control_plane.governance.features.feature_flag import FeatureFlag
from core.typing import TenantId


class FeatureRepository(Protocol):
    """
    Returns an opaque, immutable feature snapshot for a tenant.
    Application layer treats this as an opaque value (no mutation here).
    """

    def snapshot_for(self, tenant_id: TenantId) -> Any: ...

    """
    FeatureFlag repository.

    Notes
    -----
    - Keys are normalized by the governance layer; repository should store canonical key.
    - list_all() is helpful for runtime caches in the application layer.
    """

    def get_by_key(self, key: str) -> Optional[FeatureFlag]: ...
    def list_all(self, *, limit: int = 500, offset: int = 0) -> Iterable[FeatureFlag]: ...
    def save(self, flag: FeatureFlag) -> None: ...
