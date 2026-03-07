from dataclasses import dataclass
from typing import Optional, Mapping, Any
from core.typing import UnixMillis, TenantId
from core.kernel.invariants import assert_not_none
from core.errors import InvariantViolationError
from .audit_action import AuditAction

@dataclass(frozen=True, slots=True)
class AuditEvent:
    """
    Pure audit intent (no persistence details).
    """
    ts: UnixMillis
    tenant_id: Optional[TenantId]
    principal: Optional[str]       # user id, api key id, operator id, etc.
    action: AuditAction
    data: Mapping[str, Any]

    def __post_init__(self) -> None:
        assert_not_none(self.ts, "ts")
        assert_not_none(self.action, "action")
        assert_not_none(self.data, "data")
        if int(self.ts) < 0:
            raise InvariantViolationError("ts cannot be negative")