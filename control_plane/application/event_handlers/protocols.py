from typing import Protocol, Tuple, runtime_checkable

from core.events import EventEnvelope
from core.identity.uuid import UUIDProvider
from core.typing import UnixMillis


@runtime_checkable
class EventReaction(Protocol):
    """
    Pure handler for a single inbound event type.
    Given an inbound envelope + injected time/UUIDs, returns new envelopes to write.
    NO IO; no store access.
    """

    def handle(
        self,
        inbound: EventEnvelope,
        *,
        now_ms: UnixMillis,
        uuid: UUIDProvider,
    ) -> Tuple[EventEnvelope, ...]: ...


@runtime_checkable
class OutboxWriter(Protocol):
    """
    Pure outbox write port. Infra binds a concrete adapter later that uses
    core.outbox.* with a persistent store (DB/queue) while the app remains IO-free.
    """

    def write(self, topic: str, envelope: EventEnvelope, now_ms: UnixMillis) -> None: ...
