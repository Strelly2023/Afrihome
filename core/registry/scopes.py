"""
GA Enterprise Core — Registry Scopes
------------------------------------

LAYER: L3+ (LAST)
Dependencies: stdlib only

Scopes:
- PROCESS
- APPLICATION
- TENANT
- REQUEST

Resolution precedence:
REQUEST → TENANT → APPLICATION → PROCESS
"""

from enum import Enum, auto
from typing import Tuple


class RegistryScope(Enum):
    PROCESS = auto()
    APPLICATION = auto()
    TENANT = auto()
    REQUEST = auto()


DEFAULT_SCOPE_CHAIN: Tuple[RegistryScope, ...] = (
    RegistryScope.REQUEST,
    RegistryScope.TENANT,
    RegistryScope.APPLICATION,
    RegistryScope.PROCESS,
)


def scope_rank(scope: RegistryScope) -> int:
    return DEFAULT_SCOPE_CHAIN.index(scope)
