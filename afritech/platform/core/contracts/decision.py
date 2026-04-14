from __future__ import annotations

"""
AfriTech Core Contracts â€” Decision Output (GA-Sealed)

This module defines the formal contract for decision outputs produced
by decision engines within the AfriTech platform.

The DecisionContract represents the minimal, normalized shape that
ALL engines must return when producing a decision.

PURPOSE:
- Standardize decision outputs across engines
- Enable deterministic combination and replay
- Prevent leakage of engine-specific semantics

RULES:
- Pure data ONLY
- NO execution
- NO IO
- NO time
- NO precedence or governance logic
- MUST be immutable

Any change requires an ADR.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Tuple


# ============================================================================
# Contractual Decision Verdict
# ============================================================================

class ContractDecisionVerdict(Enum):
    """
    Contract-level decision verdicts.

    These verdicts describe the *form* of an engine's output,
    not the final meaning or precedence of decisions.

    Semantic interpretation and precedence are handled elsewhere
    (e.g. core/decision/combinator.py).
    """

    ALLOW = "allow"
    DENY = "deny"
    CONDITIONAL = "conditional"


# ============================================================================
# Decision Contract (Canonical Output Shape)
# ============================================================================

@dataclass(frozen=True, slots=True)
class DecisionContract:
    """
    Formal contract for decision engine outputs.

    A DecisionContract defines:
    - the engine's verdict
    - a tuple of symbolic reason codes asserted by the engine

    It does NOT:
    - apply precedence rules
    - interpret governance
    - explain final outcomes
    - reference runtime context
    - trigger effects

    This contract is consumed by higher layers for normalization
    and enforcement.
    """

    verdict: ContractDecisionVerdict
    reason_codes: Tuple[str, ...]
