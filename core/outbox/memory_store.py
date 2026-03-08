"""
GA Enterprise Core — In-Memory Outbox Store
-------------------------------------------

LAYER: L2
Dependencies: core.outbox.store_protocol, core.outbox.model, core.typing
IO: NONE
Threads/async: NONE
"""

from typing import Dict, List

from core.outbox.model import OutboxRecord, OutboxStatus
from core.outbox.store_protocol import OutboxStore
from core.typing import EventId, UnixMillis


class InMemoryOutboxStore(OutboxStore):
    def __init__(self) -> None:
        self._by_id: Dict[str, OutboxRecord] = {}
        self._by_topic: Dict[str, List[str]] = {}

    def append(self, record: OutboxRecord) -> None:
        eid = str(record.event_id)
        if eid in self._by_id:
            raise ValueError(f"OutboxRecord with event_id {eid} already exists")
        self._by_id[eid] = record
        self._by_topic.setdefault(record.topic, []).append(eid)

    def put(self, record: OutboxRecord) -> None:
        eid = str(record.event_id)
        if eid not in self._by_id:
            raise KeyError(f"OutboxRecord {eid} not found")
        self._by_id[eid] = record
        if eid not in self._by_topic.get(record.topic, []):
            for t, lst in self._by_topic.items():
                if eid in lst:
                    lst.remove(eid)
            self._by_topic.setdefault(record.topic, []).append(eid)

    def get(self, event_id: EventId):
        return self._by_id.get(str(event_id))

    def get_eligible(self, topic: str, now_ms: UnixMillis, limit: int) -> List[OutboxRecord]:
        ids = self._by_topic.get(topic, [])
        recs = [
            self._by_id[eid]
            for eid in ids
            if (r := self._by_id[eid]).status is OutboxStatus.PENDING
            and r.next_attempt_ms <= now_ms
        ]
        recs.sort(key=lambda r: (int(r.next_attempt_ms), str(r.event_id)))
        return recs[: max(0, limit)]
