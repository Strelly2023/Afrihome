from __future__ import annotations

"""
AfriTech Core Governance â€” Regimes (GA-Sealed)

This module defines governance regimes: declarative bundles of
governance rules and constraints that describe the active legal,
regulatory, or institutional context of the platform.

A GovernanceRegime does NOT enforce governance.
It declares which rules and constraints are in force.

PURPOSE:
- Represent governance contexts (e.g. INTERNAL, GDPR, PCI)
- Bind rules and constraints into a coherent legal regime
- Enable deterministic interpretation by higher layers

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
from typing import Tuple

from afritech.platform.core.governance.rules import GovernanceRule
from afritech.platform.core.governance.constraints import GovernanceConstraint


# ============================================================================
# Governance Regime (Declarative Context)
# ============================================================================

@dataclass(frozen=True, slots=True)
class GovernanceRegime:
    """
    Declarative governance regime.

    A GovernanceRegime represents a named legal or institutional
    context under which the platform operates.

    It binds together:
    - a set of normative governance rules
    - a set of absolute, non-overrideable constraints

    It does NOT:
    - interpret rules
    - enforce constraints
    - evaluate decisions
    - reference runtime state

    Regimes are selected and enforced by higher layers
    (e.g. control_plane).
    """

    regime_id: str
    rules: Tuple[GovernanceRule, ...]
    constraints: Tuple[GovernanceConstraint, ...]
