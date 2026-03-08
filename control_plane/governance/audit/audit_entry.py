# control_plane/governance/audit/audit_entry.py
import hashlib
import json
from dataclasses import dataclass

from core.kernel.invariants import assert_not_none

from .audit_event import AuditEvent
from .audit_policy import AuditPolicy


def compute_audit_content_hash(event: AuditEvent, policy: AuditPolicy | None = None) -> str:
    payload = {
        "ts": int(event.ts),
        "tenant_id": (str(event.tenant_id) if event.tenant_id else None),
        "principal": (event.principal or None),
        "action": {"category": event.action.category, "action": event.action.action},
        "data": dict((policy or AuditPolicy()).apply(event.data)),
    }
    enc = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(enc).hexdigest()


@dataclass(frozen=True, slots=True)
class AuditEntry:
    """
    Immutable audit entry prepared for persistence (still IO-free).
    """

    event: AuditEvent
    content_hash: str

    @staticmethod
    def from_event(event: AuditEvent, policy: AuditPolicy | None = None) -> "AuditEntry":
        assert_not_none(event, "event")
        return AuditEntry(event=event, content_hash=compute_audit_content_hash(event, policy))
