"""
GA Enterprise Core — Execution Context
--------------------------------------

LAYER: L1
Dependencies:
- core.context
- core.identity.uuid
- core.time.clock
- core.kernel.invariants
- core.errors

Rules:
- Immutable
- No hidden state
- No global registry
- No implicit time reads
"""

from dataclasses import dataclass

from core.context.request_context import RequestContext
from core.identity.uuid import UUIDProvider
from core.kernel.invariants import assert_not_none
from core.time.clock import Clock
from core.typing import UnixMillis


@dataclass(frozen=True, slots=True)
class ExecutionContext:
    """
    Immutable execution boundary.

    Represents:
    - Request metadata
    - Deterministic clock
    - Deterministic UUID provider
    - Write-mode state (logical only)
    """

    request_context: RequestContext
    clock: Clock
    uuid_provider: UUIDProvider
    write_mode: bool = False

    def __post_init__(self) -> None:
        assert_not_none(self.request_context, "request_context")
        assert_not_none(self.clock, "clock")
        assert_not_none(self.uuid_provider, "uuid_provider")

    def now(self) -> UnixMillis:
        return self.clock.now_ms()

    def with_write_mode(self) -> "ExecutionContext":
        from core.errors import InvariantViolationError

        if self.write_mode:
            raise InvariantViolationError("Already in write mode")
        return ExecutionContext(
            request_context=self.request_context,
            clock=self.clock,
            uuid_provider=self.uuid_provider,
            write_mode=True,
        )

    def with_request_context(self, request_context: RequestContext) -> "ExecutionContext":
        return ExecutionContext(
            request_context=request_context,
            clock=self.clock,
            uuid_provider=self.uuid_provider,
            write_mode=self.write_mode,
        )
