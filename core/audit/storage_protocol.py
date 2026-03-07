
"""
GA Enterprise Core — Audit Store Protocol
-----------------------------------------

LAYER: L2
Dependencies: core.audit.chain
IO: NONE (protocol only)
"""


from typing import List, Optional, Protocol, runtime_checkable

from core.audit.chain import ChainLink


@runtime_checkable
class AuditStore(Protocol):
    def append_link(self, link: ChainLink) -> None: ...
    def last_link(self) -> Optional[ChainLink]: ...
    def get_range(self, start_index: int, limit: int) -> List[ChainLink]: ...
