
"""
GA Enterprise Core — In-Process Event Bus
-----------------------------------------

LAYER: L2
Dependencies:
- core.events.envelope
- core.kernel.invariants

Rules:
- No threading
- No async
- No IO
- Deterministic ordering
"""


from collections import defaultdict
from typing import Callable, Dict, List

from core.events.envelope import EventEnvelope
from core.kernel.invariants import assert_not_none


EventHandler = Callable[[EventEnvelope], None]


class InProcessEventBus:
    """
    Deterministic in-process event dispatcher.
    """

    def __init__(self) -> None:
        self._handlers: Dict[str, List[EventHandler]] = defaultdict(list)

    def register(self, event_type: str, handler: EventHandler) -> None:
        assert_not_none(event_type, "event_type")
        assert_not_none(handler, "handler")
        self._handlers[event_type].append(handler)

    def dispatch(self, envelope: EventEnvelope) -> None:
        assert_not_none(envelope, "envelope")
        handlers = self._handlers.get(envelope.event.event_type, [])
        for handler in handlers:
            handler(envelope)
