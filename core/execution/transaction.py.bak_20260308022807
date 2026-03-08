
"""
GA Enterprise Core — Logical Transaction Boundary
-------------------------------------------------

LAYER: L1
Dependencies:
- core.execution.execution_context
- core.kernel.invariants

Rules:
- No DB logic
- No commit/rollback
- Pure scope wrapper
"""


from dataclasses import dataclass

from core.execution.execution_context import ExecutionContext
from core.kernel.invariants import assert_not_none


@dataclass(frozen=True, slots=True)
class TransactionBoundary:
    """
    Logical transaction boundary.

    Responsible only for:
    - Entering strict write mode
    - Returning new execution context
    """

    execution_context: ExecutionContext

    def __post_init__(self) -> None:
        assert_not_none(self.execution_context, "execution_context")

    def begin(self) -> ExecutionContext:
        return self.execution_context.with_write_mode()
