from __future__ import annotations

"""
GA Enterprise Core â€” System State Types
--------------------------------------

LAYER: L1.5 (Shared Semantic Types)
Dependencies: core.types.enums only
Deterministic: YES
Side effects: NONE
IO / Time / Network: NONE

Purpose:
- Provide a semantic alias module for system-level state enums
- Improve architectural clarity by grouping platform/system states
- Avoid duplication while enabling stable, intention-revealing imports

Design Rules:
- PURE re-exports only
- NO new enums or logic
- NO normalization helpers
- NO side effects or computation
- ABI changes flow ONLY from core.types.enums

GA NOTE:
- This module is frozen once introduced
- Any change requires an ADR
"""

from afritech.platform.core.typing.enums import (
    SystemLifecycleState,
    KernelState,
    ExecutionMode,
    SystemHealthStatus,
    FeatureFlagState,
    DataLifecycleState,
)

# ============================================================
# Public ABI (EXPLICIT + FROZEN)
# ============================================================

__all__ = [
    "SystemLifecycleState",
    "KernelState",
    "ExecutionMode",
    "SystemHealthStatus",
    "FeatureFlagState",
    "DataLifecycleState",
]
