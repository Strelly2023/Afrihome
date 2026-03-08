from dataclasses import dataclass
from typing import Mapping, Tuple

from control_plane.application.execution.models import ExecutionFrame
from core.errors import ValidationError
from core.events import EventEnvelope
from core.kernel.invariants import assert_not_none
from core.outbox.topic_grammar import validate_topic  # canonical topic grammar  # noqa

from .models import OutboxWrite, ReactionPlan
from .protocols import OutboxWriter
from .router import EventRouter


@dataclass(frozen=True, slots=True)
class EventHandlingService:
    """
    Orchestrates application reactions to platform events and outbox write planning.
      1) Route inbound envelope to a reaction (pure)
      2) Assign topics to produced envelopes (centralized policy)
      3) Validate topics with outbox grammar (pure)
      4) Optionally write to outbox via a protocol port (no IO here)
    """

    router: EventRouter
    topic_policy: Mapping[str, str]  # event_type -> outbox topic (e.g., "notifications.outbound")
    outbox: OutboxWriter | None = None

    def on_event(self, frame: ExecutionFrame, inbound: EventEnvelope) -> Tuple[OutboxWrite, ...]:
        """
        Create OutboxWrite instructions for a single inbound envelope.
        Deterministic and side-effect-free; may optionally call outbox port later.
        """
        assert_not_none(frame, "frame")
        assert_not_none(inbound, "inbound")

        plan: ReactionPlan = self.router.handle(
            inbound, now_ms=frame.ctx.now(), uuid=frame.ctx.uuid_provider
        )
        writes: list[OutboxWrite] = []
        for w in plan.writes:
            et = w.envelope.event.event_type
            topic = self.topic_policy.get(et)
            if not topic:
                raise ValidationError(f"No outbox topic policy defined for event_type={et!r}")
            vt = validate_topic(topic)  # ensure canonical grammar (pure)  # noqa
            writes.append(OutboxWrite(topic=vt, envelope=w.envelope))
        return tuple(writes)

    def write_outbox(self, frame: ExecutionFrame, writes: Tuple[OutboxWrite, ...]) -> None:
        """
        Optionally emit writes to outbox via protocol port.
        NOTE: This is still orchestration-only; OutboxWriter is a port. Infra binds persistence.
        """
        if self.outbox is None:
            return
        now = frame.ctx.now()
        for w in writes:
            self.outbox.write(w.topic, w.envelope, now_ms=now)
