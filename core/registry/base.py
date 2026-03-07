
"""
GA Enterprise Core — Registry Base Types
----------------------------------------

LAYER: L3+ (LAST)
Dependencies:
- core.errors
- core.kernel.invariants

Notes:
- Keep minimal, deterministic building blocks shared by submodules.
"""


from dataclasses import dataclass
from typing import Callable, Any


@dataclass(frozen=True, slots=True)
class ServiceDescriptor:
    name: str
    scope: str


@dataclass(frozen=True, slots=True)
class HandlerDescriptor:
    kind: str
    key: str
    scope: str
    fn_name: str
