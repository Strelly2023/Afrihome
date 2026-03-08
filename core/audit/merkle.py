"""
GA Enterprise Core — Merkle Root
--------------------------------

LAYER: L2
Dependencies: core.audit.chain (ZERO_HASH validation)
IO: NONE
Randomness: NONE
"""

import hashlib
from typing import List

from core.audit.chain import ZERO_HASH
from core.errors import InvariantViolationError


def _hex_to_bytes(h: str) -> bytes:
    if not isinstance(h, str) or len(h) != 64:
        raise InvariantViolationError("hash must be a 64-hex string")
    try:
        return bytes.fromhex(h)
    except ValueError:
        raise InvariantViolationError("hash is not valid hex")


def _pair_hash(left_hex: str, right_hex: str) -> str:
    left = _hex_to_bytes(left_hex)
    right = _hex_to_bytes(right_hex)
    return hashlib.sha256(left + right).hexdigest()


def merkle_root(hashes: List[str]) -> str:
    if not hashes:
        return ZERO_HASH
    for h in hashes:
        _hex_to_bytes(h)
    layer = list(hashes)
    while len(layer) > 1:
        next_layer: List[str] = []
        i = 0
        n = len(layer)
        while i < n:
            left = layer[i]
            right = layer[i + 1] if (i + 1) < n else layer[i]
            next_layer.append(_pair_hash(left, right))
            i += 2
        layer = next_layer
    return layer[0]
