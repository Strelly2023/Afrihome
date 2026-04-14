from __future__ import annotations
"""
AfriTech Core Registry (GA-Sealed)

This module exposes static wiring metadata for the core decision
architecture. It contains **NO runtime behavior** and must remain
immutable after GA freeze.

PURPOSE:
- Declare which core decision engines exist
- Declare canonical execution order
- Expose protocol/type references (metadata only)
- Publish immutable architectural invariants

RULES:
- Static metadata ONLY
- NO execution, evaluation, or orchestration
- NO IO, persistence, or runtime resolution
- Consumed by L3 control-plane only

Any change to this module requires an ADR.
"""



# ---------------------------------------------------------------------
# Engine catalog and classification
# ---------------------------------------------------------------------

from .engines import (
    ENGINE_NAMES,
    DECISION_ENGINES,
    HARD_DENY_ENGINES,
    SOFT_SIGNAL_ENGINES,
    OBSERVATION_ENGINES,
)


# ---------------------------------------------------------------------
# Canonical decision pipeline order
# ---------------------------------------------------------------------

from .order import (
    DECISION_ORDER,
)


# ---------------------------------------------------------------------
# Engine protocol / type metadata
# ---------------------------------------------------------------------

from .protocols import (
    ENGINE_PROTOCOLS,
)


# ---------------------------------------------------------------------
# Architectural invariants
# ---------------------------------------------------------------------

from .invariants import (
    REQUIRES_DETERMINISM,
    REQUIRES_REPLAY_SAFETY,
    DENY_WINS,
    NO_IO_ALLOWED,
    NO_DIRECT_TIME_ACCESS,
    NO_PERSISTENCE,
    NO_ORCHESTRATION,
    NO_CONTROL_PLANE_DEPENDENCY,
    NO_INFRASTRUCTURE_DEPENDENCY,
    KERNEL_IS_ABSOLUTE,
    REGISTRY_IS_STATIC,
)


# ---------------------------------------------------------------------
# Frozen public ABI
# ---------------------------------------------------------------------

__all__ = [
    # Engine universe
    "ENGINE_NAMES",
    "DECISION_ENGINES",
    "HARD_DENY_ENGINES",
    "SOFT_SIGNAL_ENGINES",
    "OBSERVATION_ENGINES",

    # Ordering
    "DECISION_ORDER",

    # Protocol metadata
    "ENGINE_PROTOCOLS",

    # Invariants
    "REQUIRES_DETERMINISM",
    "REQUIRES_REPLAY_SAFETY",
    "DENY_WINS",
    "NO_IO_ALLOWED",
    "NO_DIRECT_TIME_ACCESS",
    "NO_PERSISTENCE",
    "NO_ORCHESTRATION",
    "NO_CONTROL_PLANE_DEPENDENCY",
    "NO_INFRASTRUCTURE_DEPENDENCY",
    "KERNEL_IS_ABSOLUTE",
    "REGISTRY_IS_STATIC",
]
