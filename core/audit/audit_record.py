
"""
GA Enterprise Core — Immutable Audit Record
-------------------------------------------

LAYER: L2
Dependencies:
- core.typing
- core.kernel.invariants
- core.errors

Rules:
- Immutable
- Deterministic content hashing
- No IO, no randomness, no time reads here (timestamp injected)
"""


import json
import hashlib
from dataclasses import dataclass
from typing import Any, Mapping, Optional

from core.typing import UnixMillis, TenantId, EventId
from core.kernel.invariants import assert_not_none
from core.errors import InvariantViolationError


@dataclass(frozen=True, slots=True)
class AuditRecord:
    ts: UnixMillis
    category: str
    action: str
    tenant_id: Optional[TenantId]
    principal: Optional[str]
    event_id: Optional[EventId]
    data: Mapping[str, Any]
    content_hash: str

    def __post_init__(self) -> None:
        assert_not_none(self.ts, "ts")
        assert_not_none(self.category, "category")
        assert_not_none(self.action, "action")
        assert_not_none(self.data, "data")
        assert_not_none(self.content_hash, "content_hash")
        if self.ts < 0:
            raise InvariantViolationError("ts cannot be negative")
        if not isinstance(self.content_hash, str) or len(self.content_hash) != 64:
            raise InvariantViolationError("content_hash must be a 64-hex string")

    @staticmethod
    def create(
        *,
        ts: UnixMillis,
        category: str,
        action: str,
        tenant_id: Optional[TenantId],
        principal: Optional[str],
        event_id: Optional[EventId],
        data: Mapping[str, Any],
    ) -> "AuditRecord":
        if ts is None or category is None or action is None or data is None:
            raise InvariantViolationError("ts, category, action, and data are required")
        canonical = {
            "ts": int(ts),
            "category": str(category),
            "action": str(action),
            "tenant_id": (str(tenant_id) if tenant_id is not None else None),
            "principal": (str(principal) if principal is not None else None),
            "event_id": (str(event_id) if event_id is not None else None),
            "data": data,
        }
        encoded = json.dumps(canonical, sort_keys=True, separators=(",", ":")).encode("utf-8")
        digest = hashlib.sha256(encoded).hexdigest()
        return AuditRecord(
            ts=ts, category=category, action=action,
            tenant_id=tenant_id, principal=principal, event_id=event_id,
            data=data, content_hash=digest,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "ts": int(self.ts),
            "category": self.category,
            "action": self.action,
            "tenant_id": (str(self.tenant_id) if self.tenant_id is not None else None),
            "principal": (str(self.principal) if self.principal is not None else None),
            "event_id": (str(self.event_id) if self.event_id is not None else None),
            "data": dict(self.data),
            "content_hash": self.content_hash,
        }
