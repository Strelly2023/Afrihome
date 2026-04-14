from __future__ import annotations

"""
AfriTech Core Governance â€” Constraints (GA-Sealed)

This module defines absolute governance constraints that must
*never* be violated by the AfriTech platform.

Constraints represent hard, non-negotiable invariants of the system.
They are stronger than rules and cannot be overridden by governance
regimes, runtime decisions, or operational context.

PURPOSE:
- Declare non-overrideable invariants
- Form the immovable foundation of governance semantics
- Enable deterministic enforcement by higher layers

RULES:
- Pure data ONLY
- NO execution
- NO IO
- NO time
- NO interpretation or enforcement
- MUST be immutable

Any change requires an ADR.
"""

from dataclasses import dataclass


# ============================================================================
# Governance Constraint (Absolute Invariant)
# ============================================================================

@dataclass(frozen=True, slots=True)
class GovernanceConstraint:
    """
    Absolute governance constraint.

    A GovernanceConstraint expresses an invariant that must
    never be violated under any circumstances.

    It does NOT:
    - evaluate conditions
    - interpret policy
    - enforce itself
    - reference runtime state

    Enforcement and interpretation are handled outside core.
    """

    constraint_id: str
    description: str
