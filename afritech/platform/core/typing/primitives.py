from __future__ import annotations
"""
GA Enterprise Core â€” Deterministic Typing Primitives
---------------------------------------------------

LAYER: L1 (Foundation)
Dependencies: stdlib only
Infrastructure: NONE
Deterministic: YES

Purpose:
- Define canonical value SHAPES
- Define structural protocols
- Provide immutable data base type

Rules:
- NO validation logic
- NO error raising
- NO time, UUID, or randomness
- NO business semantics
- NO imports outside stdlib
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
# Strong Domain Identifier Types (Shapes ONLY)
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
# Time & Version Value Shapes
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

# Covariant ID type for protocols
ID_co = TypeVar("ID_co", covariant=True)


# ============================================================
# Protocol Foundations (Structural Contracts)
# ============================================================


@runtime_checkable
class Identifiable(Protocol[ID_co]):
    """
    Protocol for entities that expose a stable identifier.

    NO behavior is required.
    """
    id: ID_co


@runtime_checkable
class Versioned(Protocol):
    """
    Protocol for versioned entities.

    Version semantics are defined elsewhere.
    """
    version: Version


@runtime_checkable
class Serializable(Protocol):
    """
    Deterministic serialization contract.

    Implementations must return a JSONâ€‘serializable mapping.
    Ordering, hashing, and normalization are caller responsibilities.
    """

    def to_dict(self) -> Mapping[str, Any]: ...


# ============================================================
# Frozen Model Base (Immutable Data Carrier)
# ============================================================


@dataclass(frozen=True, slots=True)
class FrozenModel:
    """
    Base class for deterministic immutable core models.

    Enforces:
    - Immutability
    - Slot usage
    - No dynamic attributes

    Notes:
    - Subclasses must not compute nondeterministic values at init time
    - Behavior belongs in higher layers
    """
    pass


# ============================================================
# Deterministic Constants
# ============================================================

TRUE: Final[bool] = True
FALSE: Final[bool] = False
