"""
GA Enterprise Core — Outbox Store Protocol
------------------------------------------

LAYER: L2
Dependencies: core.typing, core.outbox.model
IO: NONE (protocol only)
"""

from typing import List, Optional

from core.outbox.model import OutboxRecord
from core.typing import EventId, UnixMillis


class OutboxStore:
    """
    Outbox store protocol.

    Implementations MUST be deterministic for the same sequence of inputs.
    No background behavior. No IO in core; infra layer may implement persistence.
    """

    def append(self, record: OutboxRecord) -> None: ...
    def put(self, record: OutboxRecord) -> None: ...

    def get(self, event_id: EventId) -> Optional[OutboxRecord]: ...
    def get_eligible(self, topic: str, now_ms: UnixMillis, limit: int) -> List[OutboxRecord]: ...
