from typing import Protocol, Tuple
from control_plane.governance.audit.audit_entry import AuditEntry

class AuditWriter(Protocol):
    """
    Pure outbox-facing audit write port.
    Infra implements durable storage/chaining later.
    """
    def append(self, entry: AuditEntry) -> None: ...

class AuditReader(Protocol):
    """
    Optional read port for admin/operator views (still a protocol).
    """
    def range(self, start_index: int, limit: int) -> Tuple[AuditEntry, ...]: ...