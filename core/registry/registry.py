"""
GA Enterprise Core — Core Registry Facade
-----------------------------------------

LAYER: L3+ (LAST)
Dependencies:
- core.registry.services
- core.registry.handlers
- core.registry.scopes
- core.registry.freeze_guard

Notes:
- Facade that composes service and handler registries.
- Still no globals — caller constructs CoreRegistry where needed.
"""

from dataclasses import dataclass

from core.registry.handlers import HandlerRegistry
from core.registry.services import ServiceRegistry


@dataclass(frozen=True, slots=True)
class CoreRegistry:
    services: ServiceRegistry
    handlers: HandlerRegistry

    @staticmethod
    def create() -> "CoreRegistry":
        return CoreRegistry(services=ServiceRegistry(), handlers=HandlerRegistry())
