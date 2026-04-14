from __future__ import annotations

"""
Core Test Helpers — Decision Helpers
-----------------------------------

Purpose:
- Provide canonical helper functions for constructing EngineOutcome
  objects in tests.
- Enforce GA invariants at test boundaries.
- Prevent non-string reasons from entering the core.

RULES:
- Reasons MUST be strings
- Verdicts MUST come from DecisionVerdictType
- This file is test-only but enforces production contracts
"""

from afritech.platform.core.decision.engine_outcome import EngineOutcome
from afritech.platform.core.typing.enums import DecisionVerdictType


def allow(engine: str, reason: str | None = None) -> EngineOutcome:
    """
    Construct an ALLOW EngineOutcome for tests.

    Rules:
    - reason is optional
    - when provided, it MUST be a string
    """
    return EngineOutcome(
        engine=engine,
        verdict=DecisionVerdictType.ALLOW,
        reasons=() if reason is None else (reason,),
        traces=(),
    )


def deny(engine: str, reason: str) -> EngineOutcome:
    """
    Construct a DENY EngineOutcome for tests.

    Rules:
    - reason is REQUIRED
    - reason MUST be a string
    """
    return EngineOutcome(
        engine=engine,
        verdict=DecisionVerdictType.DENY,
        reasons=(reason,),
        traces=(),
    )


def conditional(engine: str, reason: str) -> EngineOutcome:
    """
    Construct a CONDITIONAL EngineOutcome for tests.

    Exists for completeness and future coverage.
    """
    return EngineOutcome(
        engine=engine,
        verdict=DecisionVerdictType.CONDITIONAL,
        reasons=(reason,),
        traces=(),
    )


__all__ = [
    "allow",
    "deny",
    "conditional",
]