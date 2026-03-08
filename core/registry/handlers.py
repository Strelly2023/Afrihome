"""
GA Enterprise Core — Handler Registry
-------------------------------------

LAYER: L3+ (LAST)
Dependencies:
- core.registry.scopes
- core.registry.freeze_guard
- core.kernel.invariants
- core.errors

Rules:
- Deterministic registration order
- No IO / No threads / No async / No logging
- No background dispatch
"""

from dataclasses import dataclass
from typing import Callable, Dict, List, Tuple

from core.errors import ValidationError
from core.kernel.invariants import assert_not_none
from core.registry.freeze_guard import assert_registry_mutable
from core.registry.scopes import DEFAULT_SCOPE_CHAIN, RegistryScope

EventHandler = Callable[[object], None]


@dataclass(frozen=True, slots=True)
class _HandlerEntry:
    key: str
    scope: RegistryScope
    handler: EventHandler
    name: str


class HandlerRegistry:
    def __init__(self) -> None:
        # Mapping: (scope, key) -> ordered list of handler entries
        self._handlers: Dict[Tuple[RegistryScope, str], List[_HandlerEntry]] = {}

    def register(
        self,
        key: str,
        handler: EventHandler,
        *,
        scope: RegistryScope = RegistryScope.PROCESS,
        name: str | None = None,
    ) -> None:
        """
        Register a handler deterministically under (scope, key).
        Requires kernel to be mutable (freeze guard).
        """
        assert_registry_mutable()
        assert_not_none(key, "key")
        assert_not_none(handler, "handler")

        entry = _HandlerEntry(
            key=key,
            scope=scope,
            handler=handler,
            name=name or getattr(handler, "__name__", "<handler>"),
        )

        bucket_key = (scope, key)
        bucket = self._handlers.get(bucket_key)
        if bucket is None:
            # First registration for this (scope, key)
            self._handlers[bucket_key] = [entry]
            return

        # Prevent duplicate registration of the *same callable* for the same (scope, key)
        if any(h.handler is handler for h in bucket):
            raise ValidationError(f"Handler already registered for key={key!r} scope={scope.name}")
        bucket.append(entry)

    def list_for(
        self,
        key: str,
        *,
        scope_chain: Tuple[RegistryScope, ...] = DEFAULT_SCOPE_CHAIN,
    ) -> Tuple[EventHandler, ...]:
        """
        Resolve handlers for a key using the provided scope precedence chain.
        Order is preserved within each scope bucket by insertion.
        """
        assert_not_none(key, "key")

        result: List[EventHandler] = []
        for scope in scope_chain:
            bucket = self._handlers.get((scope, key))
            if not bucket:
                continue
            result.extend(h.handler for h in bucket)
        return tuple(result)

    def list_descriptors(
        self,
        key: str,
        *,
        scope_chain: Tuple[RegistryScope, ...] = DEFAULT_SCOPE_CHAIN,
    ) -> Tuple[Tuple[str, str], ...]:
        """
        Return stable (scope_name, handler_name) pairs for observability and tests.
        """
        pairs: List[Tuple[str, str]] = []
        for scope in scope_chain:
            bucket = self._handlers.get((scope, key))
            if not bucket:
                continue
            pairs.extend((scope.name, h.name) for h in bucket)
        return tuple(pairs)
