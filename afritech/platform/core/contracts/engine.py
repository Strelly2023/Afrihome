from __future__ import annotations

"""
AfriTech Core Contracts â€” Decision Engine (GA-Sealed)

This module defines the structural contract that all decision engines
within the AfriTech platform MUST satisfy.

The contract specifies:
- the identity of an engine
- the required evaluation interface
- the canonical output type

PURPOSE:
- Enforce a uniform engine interface
- Prevent semantic drift across decision engines
- Enable deterministic orchestration and combination

RULES:
- Declarative contract ONLY
- NO execution
- NO IO
- NO time
- NO engine logic
- NO orchestration
- MUST remain stable unless changed via ADR

Any change requires an ADR.
"""

from typing import Protocol, Mapping, Any

from afritech.platform.core.contracts.decision import DecisionContract


# ============================================================================
# Decision Engine Contract (Structural Interface)
# ============================================================================

class DecisionEngineContract(Protocol):
    """
    Structural contract that all decision engines must fulfill.

    This Protocol defines the minimal required interface for any
    engine that participates in AfriTech's decision system.

    It is NOT an implementation.
    It does NOT provide default behavior.
    """

    # ------------------------------------------------------------------
    # Engine Identity
    # ------------------------------------------------------------------

    engine_id: str
    """
    Stable, symbolic identifier for the engine (e.g. "rbac", "quota").

    This identifier is used for:
    - trace attribution
    - audit explanation
    - deterministic decision combination
    """

    # ------------------------------------------------------------------
    # Evaluation Interface
    # ------------------------------------------------------------------

    def evaluate(
        self,
        *,
        inputs: Mapping[str, Any],
    ) -> DecisionContract:
        """
        Evaluate a decision given canonical inputs.

        Implementations MUST:
        - be deterministic
        - be side-effect free
        - return a DecisionContract
        - NOT mutate inputs
        - NOT access IO, clocks, or infrastructure

        Interpretation, enforcement, and orchestration occur
        outside the engine.
        """
        ...
