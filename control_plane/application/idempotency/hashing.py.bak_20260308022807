import hashlib
import json
from dataclasses import dataclass
from typing import Mapping, Any

@dataclass(frozen=True, slots=True)
class CanonicalJsonResponseHasher:
    """
    Deterministic SHA-256 hasher:
      - bytes: hashed directly
      - json: canonical JSON (sort_keys=True, compact separators)
    """
    def hash_bytes(self, payload: bytes) -> str:
        return hashlib.sha256(payload).hexdigest()

    def hash_json(self, payload: Mapping[str, Any]) -> str:
        encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()