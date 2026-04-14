from __future__ import annotations

"""
AfriTech Core Contracts (GA-Sealed)

This package defines the formal, declarative contracts that govern
interaction between the AfriTech decision core and its participants
(engines, control plane, and downstream layers).

Contracts define:
- required interfaces
- canonical input and output shapes
- invariant guarantees
- declarative effect descriptions

PURPOSE:
- Establish a stable legal boundary for decision semantics
- Prevent semantic drift across engines and layers
- Enable deterministic enforcement and replay

RULES:
- Declarative exports ONLY
- NO execution
- NO IO
- NO time
- NO orchestration
- Public ABI MUST be explicit

Any change requires an ADR.
"""

# ============================================================================
# Decision Engine Contracts
# ============================================================================

from afritech.platform.core.contracts.engine import (
    DecisionEngineContract,
)

# ============================================================================
# Decision Output Contracts
# ============================================================================

from afritech.platform.core.contracts.decision import (
    DecisionContract,
    ContractDecisionVerdict,
)

# ============================================================================
# Input Contracts
# ============================================================================

from afritech.platform.core.contracts.inputs import (
    DecisionInputContract,
)

# ============================================================================
# Effect Contracts
# ============================================================================

from afritech.platform.core.contracts.effects import (
    EffectContract,
)

# ============================================================================
# Contract Invariants
# ============================================================================

from afritech.platform.core.contracts.invariants import (
    ENGINE_RETURNS_DECISION_CONTRACT,
    DETERMINISTIC_DECISIONS_REQUIRED,
    NO_SIDE_EFFECTS_IN_ENGINES,
    NO_INFRASTRUCTURE_DEPENDENCY,
)

# ============================================================================
# Frozen Public ABI
# ============================================================================

__all__ = [
    # Engine interface
    "DecisionEngineContract",

    # Decision outputs
    "DecisionContract",
    "ContractDecisionVerdict",

    # Inputs
    "DecisionInputContract",

    # Effects
    "EffectContract",

    # Invariants
    "ENGINE_RETURNS_DECISION_CONTRACT",
    "DETERMINISTIC_DECISIONS_REQUIRED",
    "NO_SIDE_EFFECTS_IN_ENGINES",
    "NO_INFRASTRUCTURE_DEPENDENCY",
]
