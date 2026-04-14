from __future__ import annotations

"""
AfriTech Core Contracts â€” Invariants (GA-Sealed)

This module defines absolute, cross-cutting invariants that apply to
ALL contract-compliant implementations within the AfriTech platform.

These invariants articulate what MUST always be true for any engine,
decision, or contract participant â€” regardless of domain, regime,
or runtime context.

PURPOSE:
- Declare non-negotiable contract guarantees
- Provide a stable foundation for enforcement and testing
- Prevent semantic drift across engines and layers

RULES:
- Pure declarations ONLY
- NO execution
- NO IO
- NO time
- NO runtime resolution
- NO side effects
- MUST remain stable unless changed via ADR

Any change requires an ADR.
"""


# ============================================================================
# Contract Invariants (Absolute Guarantees)
# ============================================================================

# Engines MUST always return values conforming to DecisionContract
ENGINE_RETURNS_DECISION_CONTRACT: bool = True

# Decision results MUST be deterministic for identical inputs
DETERMINISTIC_DECISIONS_REQUIRED: bool = True

# Engines MUST NOT perform side effects of any kind
NO_SIDE_EFFECTS_IN_ENGINES: bool = True

# Contract definitions MUST NEVER reference infrastructure concerns
NO_INFRASTRUCTURE_DEPENDENCY: bool = True


# ============================================================================
# Frozen Public ABI
# ============================================================================

__all__ = [
    "ENGINE_RETURNS_DECISION_CONTRACT",
    "DETERMINISTIC_DECISIONS_REQUIRED",
    "NO_SIDE_EFFECTS_IN_ENGINES",
    "NO_INFRASTRUCTURE_DEPENDENCY",
]
