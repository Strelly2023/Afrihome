from __future__ import annotations

"""
AfriTech Core Governance â€” Rules (GA-Sealed)

This module defines declarative governance rules that express
normative requirements of the AfriTech platform.

These rules are symbolic and non-executable.

PURPOSE:
- Declare what must be respected by the system
- Provide a common vocabulary for governance
- Enable deterministic interpretation by higher layers

RULES:
- Pure data ONLY
- NO execution
- NO IO
- NO time
- NO policy evaluation
- MUST be immutable

Any change requires an ADR.
"""

from dataclasses import dataclass, field
from typing import Mapping, Any
from types import MappingProxyType


# ============================================================================
# Governance Rule (Pure Declaration)
# ============================================================================

@dataclass(frozen=True, slots=True)
class GovernanceRule:
    """
    Declarative governance rule.

    A GovernanceRule expresses a normative requirement,
    expectation, or obligation of the system.

    It does NOT:
    - enforce itself
    - override decisions
    - evaluate conditions
    - reference runtime state

    Interpretation and enforcement are handled outside core.
    """

    rule_id: str
    description: str
    severity: str  # "hard" | "soft"
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )

    # ------------------------------------------------------------------
    # Post-init normalization (immutability guarantee)
    # ------------------------------------------------------------------

    def __post_init__(self) -> None:
        """
        Ensure metadata is deeply immutable, even if a mutable
        mapping is provided by the caller.
        """
        object.__setattr__(
            self,
            "metadata",
            MappingProxyType(dict(self.metadata)),
        )
