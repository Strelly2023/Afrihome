from __future__ import annotations

"""
Execution Audit Sink Interface
===============================

This module defines the abstract interface for execution audit sinks.

Audit sinks are responsible for persisting immutable execution audit
records produced by the execution authorization layer.

Audit persistence MUST:
- be append-only
- be immutable
- be non-lossy
- fail loudly on error

This module MUST NOT:
- compute decisions
- perform authorization
- mutate audit records
- encode infrastructure-specific logic
"""

from abc import ABC, abstractmethod

from afritech.platform.control_plane.audit.models import ExecutionAuditRecord


class ExecutionAuditSink(ABC):
    """
    Abstract base class for execution audit sinks.

    An audit sink is a boundary between authorization
    and infrastructure persistence.

    Enforcement rule:
        - Execution MUST fail if audit recording fails.
    """

    @abstractmethod
    def record(self, audit: ExecutionAuditRecord) -> None:
        """
        Persist an execution audit record.

        Implementations MUST:
        - treat `audit` as immutable
        - persist exactly once
        - never modify or replace existing records
        - raise on failure (fail-closed)

        Args:
            audit: ExecutionAuditRecord to persist

        Raises:
            Exception on any persistence failure.
            Authorization MUST abort if this method fails.
        """
        raise NotImplementedError