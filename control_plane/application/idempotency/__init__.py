"""
AfriHome Control Plane — Application/Idempotency
PHASE: 3.9 (Orchestration only)
IO: NONE | Threads/async: NONE | Deterministic: YES

Exports:
- Header constants
- BeginOutcome, CompleteOutcome, RejectOutcome
- IdempotencyKeyDeriver, IdempotencyStore, ResponseHasher
- DefaultKeyDeriver, CanonicalJsonResponseHasher
- IdempotencyService
"""

from .constants import HDR_IDEMPOTENCY_KEY
from .hashing import CanonicalJsonResponseHasher
from .models import BeginOutcome, CompleteOutcome, RejectOutcome
from .protocols import IdempotencyKeyDeriver, IdempotencyStore, ResponseHasher
from .service import DefaultKeyDeriver, IdempotencyService

__all__ = [
    "HDR_IDEMPOTENCY_KEY",
    "BeginOutcome",
    "CompleteOutcome",
    "RejectOutcome",
    "IdempotencyKeyDeriver",
    "IdempotencyStore",
    "ResponseHasher",
    "CanonicalJsonResponseHasher",
    "DefaultKeyDeriver",
    "IdempotencyService",
]
