# control_plane/repositories/audit_repository.py
from __future__ import annotations

from typing import Optional, Protocol, Tuple

from control_plane.governance.audit.audit_entry import AuditEntry


class AuditRepository(Protocol):
    """
    Pure append/read contract; infra implements persistence (Phase 5).
    Append is append-only; range is a simple read surface for operator tooling.
    """

    def append(self, entry: AuditEntry) -> None: ...
    def range(
        self, *, tenant_id: Optional[str], offset: int, limit: int
    ) -> Tuple[AuditEntry, ...]: ...
