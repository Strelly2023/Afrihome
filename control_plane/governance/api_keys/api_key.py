from dataclasses import dataclass
from typing import Optional

from core.errors import InvariantViolationError
from core.kernel.invariants import assert_not_none
from core.typing import TenantId, UnixMillis

from .api_key_id import ApiKeyId
from .api_key_scope import ApiKeyScope
from .api_key_status import ApiKeyStatus


@dataclass(frozen=True, slots=True)
class ApiKey:
    """
    Pure, immutable API key aggregate (no secrets here).
    Holds only non-sensitive identity and scope.
    """

    tenant_id: TenantId
    key_id: ApiKeyId
    name: str
    status: ApiKeyStatus
    scope: ApiKeyScope
    created_ms: UnixMillis
    updated_ms: UnixMillis
    last_used_ms: Optional[UnixMillis] = None
    description: Optional[str] = None

    def __post_init__(self) -> None:
        assert_not_none(self.tenant_id, "tenant_id")
        assert_not_none(self.key_id, "key_id")
        assert_not_none(self.name, "name")
        assert_not_none(self.status, "status")
        assert_not_none(self.scope, "scope")
        assert_not_none(self.created_ms, "created_ms")
        assert_not_none(self.updated_ms, "updated_ms")
        if int(self.created_ms) < 0 or int(self.updated_ms) < 0:
            raise InvariantViolationError("timestamps cannot be negative")
        if self.last_used_ms is not None and int(self.last_used_ms) < 0:
            raise InvariantViolationError("last_used_ms cannot be negative")
