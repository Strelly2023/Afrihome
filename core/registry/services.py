"""
GA Enterprise Core — Service Registry
-------------------------------------

LAYER: L3+ (LAST)
Dependencies:
- core.registry.scopes
- core.registry.freeze_guard
- core.errors
- core.kernel.invariants

Rules:
- No IO / No threads / No async / No logging
- No globals; instantiate ServiceRegistry
- Deterministic resolution by scope precedence
"""

from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional, Tuple

from core.errors import InvariantViolationError, ValidationError
from core.kernel.invariants import assert_not_none
from core.registry.freeze_guard import assert_registry_mutable
from core.registry.scopes import DEFAULT_SCOPE_CHAIN, RegistryScope


class ServiceNotFoundError(InvariantViolationError):
    pass


@dataclass(frozen=True, slots=True)
class _ServiceEntry:
    name: str
    scope: RegistryScope
    instance: Optional[Any] = None
    factory: Optional[Callable[[], Any]] = None


class ServiceRegistry:
    def __init__(self) -> None:
        self._services: Dict[Tuple[RegistryScope, str], _ServiceEntry] = {}

    def register_instance(
        self, name: str, instance: Any, scope: RegistryScope = RegistryScope.PROCESS
    ) -> None:
        assert_registry_mutable()
        assert_not_none(name, "name")
        assert_not_none(instance, "instance")
        key = (scope, name)
        if key in self._services:
            raise ValidationError(f"Service {name!r} already registered for scope={scope.name}")
        self._services[key] = _ServiceEntry(name=name, scope=scope, instance=instance, factory=None)

    def register_factory(
        self, name: str, factory: Callable[[], Any], scope: RegistryScope = RegistryScope.PROCESS
    ) -> None:
        assert_registry_mutable()
        assert_not_none(name, "name")
        assert_not_none(factory, "factory")
        key = (scope, name)
        if key in self._services:
            raise ValidationError(f"Service {name!r} already registered for scope={scope.name}")
        self._services[key] = _ServiceEntry(name=name, scope=scope, instance=None, factory=factory)

    def resolve(
        self,
        name: str,
        *,
        scope_chain: Tuple[RegistryScope, ...] = DEFAULT_SCOPE_CHAIN,
        construct: bool = True,
    ) -> Any:
        assert_not_none(name, "name")
        for scope in scope_chain:
            entry = self._services.get((scope, name))
            if entry is None:
                continue
            if entry.instance is not None:
                return entry.instance
            if entry.factory is not None:
                return entry.factory() if construct else entry.factory
        raise ServiceNotFoundError(
            f"Service {name!r} not found for scopes={[s.name for s in scope_chain]}"
        )

    def try_resolve(
        self,
        name: str,
        *,
        scope_chain: Tuple[RegistryScope, ...] = DEFAULT_SCOPE_CHAIN,
        construct: bool = True,
    ) -> Optional[Any]:
        try:
            return self.resolve(name, scope_chain=scope_chain, construct=construct)
        except ServiceNotFoundError:
            return None

    def list_names(self) -> Tuple[str, ...]:
        seen = []
        for _scope, name in self._services.keys():
            if name not in seen:
                seen.append(name)
        return tuple(seen)

    def list_scoped(self) -> Tuple[Tuple[RegistryScope, str], ...]:
        return tuple(self._services.keys())
