"""
GA Enterprise Core — Audit Chain
--------------------------------

LAYER: L2
Dependencies:
- core.kernel.invariants
- core.errors

Rules:
- Immutable chain links
- Pure hashing
- No IO
"""

import hashlib
from dataclasses import dataclass
from typing import Optional

from core.errors import InvariantViolationError
from core.kernel.invariants import assert_not_none

ZERO_HASH: str = "0" * 64


def _hex_to_bytes(h: str) -> bytes:
    if not isinstance(h, str) or len(h) != 64:
        raise InvariantViolationError("hash must be a 64-hex string")
    try:
        return bytes.fromhex(h)
    except ValueError:
        raise InvariantViolationError("hash is not valid hex")


@dataclass(frozen=True, slots=True)
class ChainLink:
    index: int
    prev_hash: str
    record_hash: str
    chain_hash: str

    def __post_init__(self) -> None:
        if self.index < 0:
            raise InvariantViolationError("index cannot be negative")
        _hex_to_bytes(self.prev_hash)
        _hex_to_bytes(self.record_hash)
        _hex_to_bytes(self.chain_hash)


def make_chain_link(prev: Optional["ChainLink"], record_hash: str) -> "ChainLink":
    assert_not_none(record_hash, "record_hash")
    _hex_to_bytes(record_hash)
    if prev is None:
        prev_hash = ZERO_HASH
        index = 0
    else:
        prev_hash = prev.chain_hash
        index = prev.index + 1
    chain_hash = hashlib.sha256(_hex_to_bytes(prev_hash) + _hex_to_bytes(record_hash)).hexdigest()
    return ChainLink(
        index=index, prev_hash=prev_hash, record_hash=record_hash, chain_hash=chain_hash
    )
