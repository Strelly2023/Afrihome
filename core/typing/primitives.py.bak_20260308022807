
"""
GA Enterprise Core — Deterministic Typing Primitives
----------------------------------------------------

LAYER: L0
Dependencies: stdlib only
Infrastructure: NONE
Deterministic: YES

Rules:
- No runtime mutation helpers
- No reflection
- No dynamic type factories
- Protocol-first design
"""


from dataclasses import dataclass
from typing import (
    Any,
    Final,
    Mapping,
    NewType,
    Protocol,
    TypeVar,
    runtime_checkable,
)

# ============================================================
# Strong Domain Types
# ============================================================

TenantId = NewType("TenantId", str)
UserId = NewType("UserId", str)
RequestId = NewType("RequestId", str)
EventId = NewType("EventId", str)
CorrelationId = NewType("CorrelationId", str)
CausationId = NewType("CausationId", str)
AggregateId = NewType("AggregateId", str)
Permission = NewType("Permission", str)
RoleName = NewType("RoleName", str)

# ============================================================
# Time & Version Types
# ============================================================

UnixMillis = NewType("UnixMillis", int)
Version = NewType("Version", int)

# ============================================================
# Generic Type Variables
# ============================================================

T = TypeVar("T")
K = TypeVar("K")
V = TypeVar("V")
R = TypeVar("R")

# Optional: ID type variable for Identifiable
ID_co = TypeVar("ID_co", covariant=True)

# ============================================================
# Protocol Foundations
# ============================================================

@runtime_checkable
class Identifiable(Protocol[ID_co]):
    """
    Protocol for entities that expose an ID.
    Keeps the field name stable for ergonomics in the core.
    """
    id: ID_co


@runtime_checkable
class Versioned(Protocol):
    """
    Protocol for version-controlled entities.
    """
    version: Version


@runtime_checkable
class Serializable(Protocol):
    """
    Deterministic serialization contract.

    Implementations should return a JSON-serializable mapping.
    The caller may normalize keys and order when hashing (e.g., via a stable dumper).
    """
    def to_dict(self) -> Mapping[str, Any]: ...

# ============================================================
# Frozen Model Base
# ============================================================

@dataclass(frozen=True, slots=True)
class FrozenModel:
    """
    Base class for deterministic immutable models.

    Enforces:
    - Immutability (frozen dataclass)
    - Slot usage (predictable memory layout)
    - No dynamic attributes

    Notes:
    - Subclasses should avoid storing non-deterministic values at init time.
    - Prefer pure data + explicit injected dependencies in higher layers.
    """
    pass

# ============================================================
# Deterministic Constants
# ============================================================

TRUE: Final[bool] = True
FALSE: Final[bool] = False
