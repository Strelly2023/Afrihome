from dataclasses import dataclass
from typing import Dict, Tuple

from core.events import EventEnvelope
from core.identity.uuid import UUIDProvider
from core.kernel.invariants import assert_not_none
from core.typing import UnixMillis

from .models import OutboxWrite, ReactionPlan
from .protocols import EventReaction


@dataclass(frozen=True, slots=True)
class EventRouter:
    """
    Deterministic mapping: event_type -> EventReaction.
    Router itself performs no IO; handlers remain pure.
    """

    _reactions: Dict[str, EventReaction]

    def handle(
        self, inbound: EventEnvelope, *, now_ms: UnixMillis, uuid: UUIDProvider
    ) -> ReactionPlan:
        assert_not_none(inbound, "inbound")
        assert_not_none(uuid, "uuid")
        assert_not_none(now_ms, "now_ms")
        et = inbound.event.event_type
        handler = self._reactions.get(et)
        if handler is None:
            return ReactionPlan(writes=())  # no-op if no reaction registered
        out = handler.handle(inbound, now_ms=now_ms, uuid=uuid)
        # Reactions return envelopes; topics are assigned by the service/policy in the next step.
        # Here we keep envelopes only; Outbox topic binding occurs in EventHandlingService.
        return ReactionPlan(
            writes=tuple(OutboxWrite(topic="", envelope=e) for e in out)
        )  # topic to be filled later

    def descriptors(self) -> Tuple[str, ...]:
        return tuple(self._reactions.keys())
