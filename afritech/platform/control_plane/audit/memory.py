from __future__ import annotations
#afritech/platform/control_plane/audit/memory.py
from typing import List
from dataclasses import dataclass

from afritech.platform.control_plane.audit.models import ExecutionAuditRecord
from afritech.platform.control_plane.audit.sink import ExecutionAuditSink


class AuditSinkFailure(RuntimeError):
    """Raised when the audit sink fails to persist a record."""


@dataclass
class InMemoryExecutionAuditSink(ExecutionAuditSink):
    """
    In-memory audit sink.

    Characteristics:
    - append-only
    - deterministic
    - test-inspectable
    - non-durable (by design)
    """

    records: List[ExecutionAuditRecord]
    fail_writes: bool = False

    def __init__(self) -> None:
        self.records = []
        self.fail_writes = False

    def record(self, audit: ExecutionAuditRecord) -> None:
        """
        Persist an audit record in memory.

        Raises:
            AuditSinkFailure if fail_writes is enabled.
        """

        if self.fail_writes:
            raise AuditSinkFailure(
                "audit sink is configured to fail writes"
            )

        # Append-only: never modify, never replace
        self.records.append(audit)
