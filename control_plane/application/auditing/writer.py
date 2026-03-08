# control_plane/application/auditing/writer.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Optional

from control_plane.application.execution.models import ExecutionFrame
from control_plane.governance.audit.audit_action import AuditAction
from control_plane.governance.audit.audit_entry import AuditEntry
from control_plane.governance.audit.audit_event import AuditEvent
from control_plane.governance.audit.audit_policy import AuditPolicy
from control_plane.repositories.audit_repository import AuditRepository
from core.kernel.invariants import assert_not_none
from core.typing import UnixMillis


@dataclass(frozen=True, slots=True)
class AuditWriter:
    """
    Deterministic, IO-free audit orchestrator.
    - Builds AuditEvent/AuditEntry (Governance).
    - Appends via AuditRepository (port).

    Principal selection order (explicit):
      1) explicit `principal` argument if provided
      2) frame.actor.principal (e.g., API key id / service name)
      3) str(frame.actor.user_id) when present
      4) else None
    """

    repo: AuditRepository
    policy: AuditPolicy = AuditPolicy()

    def write(
        self,
        frame: ExecutionFrame,
        *,
        category: str,
        action: str,
        data: Mapping[str, Any],
        principal: Optional[str] = None,
        ts_ms: Optional[UnixMillis] = None,
    ) -> AuditEntry:
        assert_not_none(frame, "frame")
        assert_not_none(category, "category")
        assert_not_none(action, "action")
        assert_not_none(data, "data")

        evt = AuditEvent(
            ts=int(ts_ms if ts_ms is not None else frame.timestamp_ms),
            tenant_id=frame.tenant_id,
            principal=(
                principal
                if principal is not None
                else (
                    frame.actor.principal
                    or (str(frame.actor.user_id) if frame.actor.user_id else None)
                )
            ),
            action=AuditAction(category=category, action=action),
            data=dict(data),
        )
        entry = AuditEntry.from_event(evt, self.policy)
        self.repo.append(entry)  # protocol call only; infra persists later
        return entry
