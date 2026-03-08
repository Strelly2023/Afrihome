from dataclasses import dataclass
from typing import Iterable, Tuple
from core.kernel.invariants import assert_not_none
from core.events import DomainEvent, EventHeaders, EventEnvelope
from control_plane.application.execution.models import ExecutionFrame
from .protocols import WindowCalculator

@dataclass(frozen=True, slots=True)
class AggregationOrchestrator:
    """
    Builds pure aggregation request envelopes for one or more windows.
    Downstream workers (Phases 5–7) will read these and compute counters.
    """
    event_type: str = "usage.aggregate.requested"

    def plan_for_windows(
        self,
        frame: ExecutionFrame,
        *,
        key: str,
        window_calc: WindowCalculator,
        windows: Iterable[str],
        backfill: int = 0,
    ) -> Tuple[EventEnvelope, ...]:
        """
        Create one EventEnvelope per requested window, including optional backfill
        for N previous windows of the same kind (deterministically computed).
        """
        assert_not_none(frame, "frame")
        assert_not_none(key, "key")
        assert_not_none(window_calc, "window_calc")

        k = key.strip()
        if not k:
            from core.errors import ValidationError
            raise ValidationError("aggregation key must be a non-empty string")

        now_ms = int(frame.ctx.now())
        out: list[EventEnvelope] = []

        for wkind in windows:
            # Current window
            wid, ws, we = window_calc.compute(now_ms=now_ms, window=wkind)
            out.append(self._build_envelope(frame, k, wkind, wid, ws, we))

            # Deterministic backfill: step left by window size using end->start deltas
            # (Workers are responsible for idempotency; this is pure planning.)
            # We reuse compute() against synthetic timestamps to avoid ambient time.
            last_start = ws
            for _ in range(max(0, int(backfill))):
                # Move one unit back: choose ts one millisecond before previous start
                # to land in the previous window deterministically.
                prev_ts = int(last_start) - 1
                pwid, pws, pwe = window_calc.compute(now_ms=prev_ts, window=wkind)
                out.append(self._build_envelope(frame, k, wkind, pwid, pws, pwe))
                last_start = pws

        return tuple(out)

    def _build_envelope(
        self,
        frame: ExecutionFrame,
        key: str,
        window_kind: str,
        window_id: str,
        ws: int,
        we: int,
    ) -> EventEnvelope:
        event = DomainEvent(
            event_id=frame.ctx.uuid_provider.new_event_id(),
            event_type=self.event_type,
            payload={
                "tenant_id": str(frame.tenant_id),
                "key": key,
                "window_kind": window_kind,
                "window": {
                    "id": window_id,
                    "start_ms": int(ws),
                    "end_ms": int(we),
                },
            },
        )
        headers = EventHeaders(
            correlation_id=frame.correlation_id,
            causation_id=frame.causation_id,
            timestamp_ms=frame.timestamp_ms,
            tenant_id=frame.tenant_id,
        )
        return EventEnvelope.create(event=event, headers=headers)