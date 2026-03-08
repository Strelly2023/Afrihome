"""
GA Enterprise Core — Registry (Final Binding Layer)

LAYER: L3+ (LAST)

Purpose:
- Deterministic binding of services and handlers
- Scoped resolution (REQUEST → TENANT → APPLICATION → PROCESS)
- Freeze guard: no mutations after kernel.freeze

Rules:
- No IO / No threads / No async / No logging
- No globals, no singletons: compose a CoreRegistry where needed
- Deterministic order preserved by insertion
"""

from .freeze_guard import assert_registry_mutable
from .handlers import HandlerRegistry
from .registry import CoreRegistry
from .scopes import DEFAULT_SCOPE_CHAIN, RegistryScope, scope_rank
from .services import ServiceNotFoundError, ServiceRegistry

__all__ = [
    "RegistryScope",
    "DEFAULT_SCOPE_CHAIN",
    "scope_rank",
    "ServiceRegistry",
    "ServiceNotFoundError",
    "HandlerRegistry",
    "CoreRegistry",
    "assert_registry_mutable",
]
