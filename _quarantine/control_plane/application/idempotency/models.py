from dataclasses import dataclass
from typing import Optional
from core.guards.idempotency import IdempotencyRecord  # pure, immutable core model  # noqa
# (No IO here; this module orchestrates transitions only.)                          # noqa

@dataclass(frozen=True, slots=True)
class BeginOutcome:
    """
    Result of IdempotencyService.begin(...).
    - record: the (possibly updated) IdempotencyRecord
    - created_new: True iff this invocation created a new IN_PROGRESS record
    - replay: True iff an earlier COMPLETED record already exists (same key)
    - key: stable idempotency key used
    """
    record: IdempotencyRecord
    created_new: bool
    replay: bool
    key: str

@dataclass(frozen=True, slots=True)
class CompleteOutcome:
    """
    Result of IdempotencyService.complete(...).
    - record: COMPLETED record (immutable)
    - key: idempotency key
    """
    record: IdempotencyRecord
    key: str

@dataclass(frozen=True, slots=True)
class RejectOutcome:
    """
    Result of IdempotencyService.reject(...).
    - record: REJECTED record (immutable)
    - key: idempotency key
    """
    record: IdempotencyRecord
    key: str