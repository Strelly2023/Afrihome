from __future__ import annotations

"""
AfriTech Core Contracts â€” Decision Inputs (GA-Sealed)

This module defines the canonical input contract for all decision
engines within the AfriTech platform.

The DecisionInputContract establishes the minimal, stable shape of
inputs required to evaluate decisions deterministically.

PURPOSE:
- Standardize decision inputs across engines
- Ensure replay-safe and deterministic evaluation
- Prevent ad-hoc or implicit input structures

RULES:
- Pure data ONLY
- NO execution
- NO IO
- NO time
- NO evaluation or interpretation
- MUST be immutable

Any change requires an ADR.
"""

from dataclasses import dataclass, field
from typing import Mapping, Any
from types import MappingProxyType


# ============================================================================
# Decision Input Contract (Canonical, Immutable)
# ============================================================================

@dataclass(frozen=True, slots=True)
class DecisionInputContract:
    """
    Canonical input contract for decision engine evaluation.

    A DecisionInputContract defines:
    - the subject performing an action
    - the action being requested
    - the target resource
    - opaque, structured attributes providing context

    It does NOT:
    - interpret attributes
    - resolve identities
    - perform validation
    - impose policy semantics

    Interpretation and enforcement occur elsewhere.
    """

    subject_id: str
    action: str
    resource: str
    attributes: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )

    # ------------------------------------------------------------------
    # Post-init normalization (deep immutability guarantee)
    # ------------------------------------------------------------------

    def __post_init__(self) -> None:
        """
        Ensure attributes are deeply immutable, even if a mutable
        mapping is provided by the caller.
        """
        object.__setattr__(
            self,
            "attributes",
            MappingProxyType(dict(self.attributes)),
        )
