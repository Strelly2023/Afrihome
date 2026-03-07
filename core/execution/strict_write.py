
"""
GA Enterprise Core — Strict Write Enforcement
---------------------------------------------

LAYER: L1
Dependencies:
- core.execution.execution_context
- core.errors

Purpose:
- Prevent write operations outside explicit write mode.
"""


from core.execution.execution_context import ExecutionContext
from core.errors import StrictWriteViolationError


class StrictWriteMode:
    """
    Write enforcement authority.
    """

    @staticmethod
    def require_write(ctx: ExecutionContext) -> None:
        if not ctx.write_mode:
            raise StrictWriteViolationError()
