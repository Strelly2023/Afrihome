from typing import Any, Mapping, Optional, Protocol, runtime_checkable

from core.guards.idempotency import IdempotencyRecord  # core model  # noqa


@runtime_checkable
class IdempotencyStore(Protocol):
    """
    Pure repository protocol for idempotency records.
    Infra binds a concrete adapter later (DB/Redis/etc.).
    """

    def get(self, key: str) -> Optional[IdempotencyRecord]: ...
    def put(self, record: IdempotencyRecord) -> None: ...


@runtime_checkable
class IdempotencyKeyDeriver(Protocol):
    """
    Deterministic derivation of an idempotency key.
    Must be pure (no IO, no randomness).
    """

    def derive(
        self,
        *,
        header_value: Optional[str],
        tenant_id: str,
        method: Optional[str],
        route: Optional[str],
        scope: Mapping[str, str] | None = None,
    ) -> str: ...


@runtime_checkable
class ResponseHasher(Protocol):
    """
    Deterministic response hashing contract (produces a 64-hex digest).
    Implementations must be pure and stable.
    """

    def hash_bytes(self, payload: bytes) -> str: ...
    def hash_json(self, payload: Mapping[str, Any]) -> str: ...
