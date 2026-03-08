from dataclasses import dataclass
from typing import Mapping

from control_plane.application.execution.models import ExecutionFrame
from core.events import DomainEvent, EventEnvelope, EventHeaders
from core.kernel.invariants import assert_not_none

from .models import UsageIncrement, WindowedUsagePlan
from .protocols import WindowCalculator


@dataclass(frozen=True, slots=True)
class UsageRecorder:
    """
    Orchestration-only recorder that turns a usage increment into a pure EventEnvelope.
    No IO; workers later persist/aggregate via outbox/infra.
    """

    event_type: str = "usage.recorded"

    def record(
        self,
        frame: ExecutionFrame,
        *,
        increment: UsageIncrement,
        window_calc: WindowCalculator,
        window_kind: str,
    ) -> EventEnvelope:
        assert_not_none(frame, "frame")
        assert_not_none(increment, "increment")
        assert_not_none(window_calc, "window_calc")
        if not increment.key or not increment.key.strip():
            from core.errors import ValidationError

            raise ValidationError("usage key must be a non-empty string")

        now_ms = int(frame.ctx.now())
        window_id, ws, we = window_calc.compute(now_ms=now_ms, window=window_kind)

        plan = WindowedUsagePlan(
            key=increment.key.strip(),
            amount=int(increment.amount),
            window_id=window_id,
            window_start_ms=ws,
            window_end_ms=we,
            attributes=(
                dict(increment.attributes) if isinstance(increment.attributes, Mapping) else {}
            ),
        )

        event = DomainEvent(
            event_id=frame.ctx.uuid_provider.new_event_id(),
            event_type=self.event_type,
            payload={
                "tenant_id": str(frame.tenant_id),
                "key": plan.key,
                "amount": plan.amount,
                "window": {
                    "id": plan.window_id,
                    "start_ms": int(plan.window_start_ms),
                    "end_ms": int(plan.window_end_ms),
                },
                "attributes": dict(plan.attributes),
            },
        )
        headers = EventHeaders(
            correlation_id=frame.correlation_id,
            causation_id=frame.causation_id,
            timestamp_ms=frame.timestamp_ms,
            tenant_id=frame.tenant_id,
        )
        # Deterministic envelope with content hash for outbox/audit
        return EventEnvelope.create(event=event, headers=headers)
