from __future__ import annotations

"""
GA Enterprise Core â€” Typing Public Interface
-------------------------------------------

LAYER: L1 (Foundation)
Deterministic: YES
Side effects: NONE

Purpose:
- Expose canonical typing primitives used across the core
- Provide a stable, GA-sealed public typing surface
- Aggregate value-shapes, protocols, and semantic enums

Rules:
- This file defines the PUBLIC typing ABI
- All additions are GA-sensitive and ADR-gated
- No logic, no side effects, no imports from L2 engines
"""

# ---------------------------------------------------------------------
# Core typing primitives (value shapes, protocols)
# ---------------------------------------------------------------------

from .primitives import (
    TenantId,
    UserId,
    RequestId,
    EventId,
    CorrelationId,
    CausationId,
    AggregateId,
    Permission,
    RoleName,
    UnixMillis,
    Version,
    T,
    K,
    V,
    R,
    ID_co,
    Identifiable,
    Versioned,
    Serializable,
    FrozenModel,
    TRUE,
    FALSE,
)

# ---------------------------------------------------------------------
# Canonical semantic enums (GA-sealed)
# ---------------------------------------------------------------------

from .enums import (
    EngineId,
    Effect,
    DecisionVerdictType,
    ConsentState,
    ReasonCategory,
    SystemLifecycleState,
    KernelState,
    ExecutionMode,
    SystemHealthStatus,
    FeatureFlagState,
    DataLifecycleState,
)

# ---------------------------------------------------------------------
# System state alias module (pure re-export)
# ---------------------------------------------------------------------

from .system import (
    SystemLifecycleState,
    KernelState,
    ExecutionMode,
    SystemHealthStatus,
    FeatureFlagState,
    DataLifecycleState,
)

# ---------------------------------------------------------------------
# Public ABI (EXPLICIT + FROZEN)
# ---------------------------------------------------------------------

__all__ = [
    # -----------------------------------------------------------------
    # Core value types & identifiers
    # -----------------------------------------------------------------
    "TenantId",
    "UserId",
    "RequestId",
    "EventId",
    "CorrelationId",
    "CausationId",
    "AggregateId",
    "Permission",
    "RoleName",
    "UnixMillis",
    "Version",

    # -----------------------------------------------------------------
    # Typing helpers (generics, protocols)
    # -----------------------------------------------------------------
    "T",
    "K",
    "V",
    "R",
    "ID_co",
    "Identifiable",
    "Versioned",
    "Serializable",

    # -----------------------------------------------------------------
    # Deterministic base model
    # -----------------------------------------------------------------
    "FrozenModel",

    # -----------------------------------------------------------------
    # Deterministic constants
    # -----------------------------------------------------------------
    "TRUE",
    "FALSE",

    # -----------------------------------------------------------------
    # Canonical semantic enums
    # -----------------------------------------------------------------
    "EngineId",
    "Effect",
    "DecisionVerdictType",
    "ConsentState",
    "ReasonCategory",

    # -----------------------------------------------------------------
    # System state enums (also available via typing.system)
    # -----------------------------------------------------------------
    "SystemLifecycleState",
    "KernelState",
    "ExecutionMode",
    "SystemHealthStatus",
    "FeatureFlagState",
    "DataLifecycleState",
]
