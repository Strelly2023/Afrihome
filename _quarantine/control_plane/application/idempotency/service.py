from dataclasses import dataclass
from typing import Mapping, Optional, Any
from core.kernel.invariants import assert_not_none
from core.errors import ValidationError
from control_plane.application.execution.models import ExecutionFrame
from .constants import HDR_IDEMPOTENCY_KEY
from .models import BeginOutcome, CompleteOutcome, RejectOutcome
from .protocols import IdempotencyKeyDeriver, IdempotencyStore, ResponseHasher

# Core pure idempotency transitions (immutable state machine)
from core.guards.idempotency import (
    IdempotencyRecord,
    IdempotencyStatus,
    idempotency_start,
    idempotency_complete,
    idempotency_reject,
    is_replay_of,
)  # [1](https://teamglobalexp-my.sharepoint.com/personal/djuma_kikombe2_teamglobalexp_com/Documents/Microsoft%20Copilot%20Chat%20Files/phases.txt)

# Optional routing hints (Phase 4 may set these on normalized headers)
HDR_METHOD = "x-method"
HDR_ROUTE  = "x-route"

@dataclass(frozen=True, slots=True)
class DefaultKeyDeriver:
    """
    Stable, tenant-scoped idempotency key grammar:
      idem:{tenant}:{header_or_derived}
    If the header 'x-idempotency-key' is present, we use it directly (lowercased/trimmed).
    Otherwise we deterministically derive: {method}:{route}
    Optional 'scope' k=v pairs (sorted by key) can further disambiguate.
    """
    prefix: str = "idem"

    def derive(
        self,
        *,
        header_value: Optional[str],
        tenant_id: str,
        method: Optional[str],
        route: Optional[str],
        scope: Mapping[str, str] | None = None,
    ) -> str:
        base = (header_value or "").strip().lower()
        if not base:
            m = (method or "").strip().lower() or "-"
            r = (route  or "").strip().lower() or "-"
            base = f"{m}:{r}"
        parts = [self.prefix, tenant_id, base]
        if scope:
            for k in sorted(scope.keys()):
                v = str(scope[k]).strip().lower()
                parts.append(f"{k.strip().lower()}={v}")
        return ":".join(parts)

@dataclass(frozen=True, slots=True)
class IdempotencyService:
    """
    Orchestration wrapper around core idempotency transitions (pure).
      1) Derive key (header or deterministic fallback)
      2) Read existing record via IdempotencyStore (protocol)
      3) Apply core transitions (start/complete/reject)
      4) Persist via store (protocol) if requested
    NOTE:
      - No IO here; store is an interface only.
      - Response payloads are NOT stored here; only 'response_hash' is persisted.
        Infra can map 'response_hash' to cached payload later if desired.
    """
    store: IdempotencyStore
    deriver: IdempotencyKeyDeriver

    # --------- High-level API ---------

    def begin(
        self,
        frame: ExecutionFrame,
        *,
        headers: Mapping[str, str],
        scope: Mapping[str, str] | None = None,
        persist: bool = True,
    ) -> BeginOutcome:
        """
        Signal the start (or replay) of an idempotent operation.
        Returns an outcome indicating whether processing should proceed.
        """
        assert_not_none(frame, "frame")
        assert_not_none(headers, "headers")

        key = self._derive_key(frame, headers, scope)
        existing = self.store.get(key)

        # Pure core transition — returns (record, created_new_flag)
        rec, created_new = idempotency_start(existing, key=key, now_ms=frame.ctx.now())  # [1](https://teamglobalexp-my.sharepoint.com/personal/djuma_kikombe2_teamglobalexp_com/Documents/Microsoft%20Copilot%20Chat%20Files/phases.txt)

        # "Replay" means we already have a COMPLETED record (response can be fetched via response_hash)
        replay = is_replay_of(existing, response_hash=None)  # True if existing is COMPLETED  # [1](https://teamglobalexp-my.sharepoint.com/personal/djuma_kikombe2_teamglobalexp_com/Documents/Microsoft%20Copilot%20Chat%20Files/phases.txt)

        if persist:
            # Persist the new/updated snapshot (protocol; infra binds real store)
            self.store.put(rec)

        return BeginOutcome(record=rec, created_new=created_new, replay=replay, key=key)

    def complete_with_bytes(
        self,
        frame: ExecutionFrame,
        *,
        key: Optional[str],
        payload: bytes,
        hasher: ResponseHasher,
        persist: bool = True,
    ) -> CompleteOutcome:
        """
        Mark the idempotent operation as COMPLETED using a deterministic hash of bytes payload.
        """
        assert_not_none(frame, "frame")
        assert_not_none(payload, "payload")
        assert_not_none(hasher, "hasher")

        k = key or self._derive_key(frame, frame.headers, None)
        existing = self._require_existing(k)
        digest = hasher.hash_bytes(payload)

        # Pure core transition to COMPLETED
        rec = idempotency_complete(existing, response_hash=digest, now_ms=frame.ctx.now())  # [1](https://teamglobalexp-my.sharepoint.com/personal/djuma_kikombe2_teamglobalexp_com/Documents/Microsoft%20Copilot%20Chat%20Files/phases.txt)

        if persist:
            self.store.put(rec)
        return CompleteOutcome(record=rec, key=k)

    def complete_with_json(
        self,
        frame: ExecutionFrame,
        *,
        key: Optional[str],
        payload: Mapping[str, Any],
        hasher: ResponseHasher,
        persist: bool = True,
    ) -> CompleteOutcome:
        """
        Mark the idempotent operation as COMPLETED using a deterministic hash of a JSON-serializable mapping.
        """
        assert_not_none(frame, "frame")
        assert_not_none(payload, "payload")
        assert_not_none(hasher, "hasher")

        k = key or self._derive_key(frame, frame.headers, None)
        existing = self._require_existing(k)
        digest = hasher.hash_json(payload)

        rec = idempotency_complete(existing, response_hash=digest, now_ms=frame.ctx.now())  # [1](https://teamglobalexp-my.sharepoint.com/personal/djuma_kikombe2_teamglobalexp_com/Documents/Microsoft%20Copilot%20Chat%20Files/phases.txt)

        if persist:
            self.store.put(rec)
        return CompleteOutcome(record=rec, key=k)

    def reject(
        self,
        frame: ExecutionFrame,
        *,
        key: Optional[str],
        reason: str,
        persist: bool = True,
    ) -> RejectOutcome:
        """
        Mark the idempotent operation as REJECTED with a deterministic reason.
        """
        assert_not_none(frame, "frame")
        if not reason or not reason.strip():
            raise ValidationError("reject reason must be a non-empty string")

        k = key or self._derive_key(frame, frame.headers, None)
        existing = self.store.get(k)

        # Pure core transition to REJECTED (works with or without existing)
        rec = idempotency_reject(existing, key=k, reason=reason.strip(), now_ms=frame.ctx.now())  # [1](https://teamglobalexp-my.sharepoint.com/personal/djuma_kikombe2_teamglobalexp_com/Documents/Microsoft%20Copilot%20Chat%20Files/phases.txt)

        if persist:
            self.store.put(rec)
        return RejectOutcome(record=rec, key=k)

    # --------- Internals ---------

    def _derive_key(self, frame: ExecutionFrame, headers: Mapping[str, str], scope: Mapping[str, str] | None) -> str:
        hv = (headers.get(HDR_IDEMPOTENCY_KEY) or "").strip() or None
        method = (headers.get(HDR_METHOD) or "").strip() or None
        route  = (headers.get(HDR_ROUTE)  or "").strip() or None
        return self.deriver.derive(
            header_value=hv,
            tenant_id=str(frame.tenant_id),
            method=method,
            route=route,
            scope=scope,
        )

    def _require_existing(self, key: str) -> IdempotencyRecord:
        existing = self.store.get(key)
        if existing is None:
            raise ValidationError(f"Idempotency record not found for key={key!r}; call begin() first")
        return existing