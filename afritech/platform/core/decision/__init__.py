from __future__ import annotations

"""
AfriTech Core — Decision (GA-SEALED)
===================================

GA-SEALED

LAYER: L2 (Pure Semantic Composition Surface)
Deterministic: YES
Side effects: NONE

PURPOSE:
- Expose the canonical, normalized Decision surface
- Provide deterministic combination of engine outcomes
- Enforce deny-wins semantics across engines

GA RULES:
- Public API is defined ONLY via __all__
- No engine-specific knowledge
- No orchestration or governance interpretation
- No IO, clocks, persistence, or runtime resolution

This module is a semantic boundary.
Its contents are frozen and constitute platform law.
Any change requires an Architecture Decision Record (ADR).
"""

# ---------------------------------------------------------------------
# Canonical decision model
# ---------------------------------------------------------------------

from afritech.platform.core.decision.decision import (
    Decision,
    DecisionVerdict,
)

# ---------------------------------------------------------------------
# Decision explanation primitives
# ---------------------------------------------------------------------

from afritech.platform.core.decision.reason import (
    DecisionReason,
)

from afritech.platform.core.decision.trace import (
    DecisionTrace,
)

# ---------------------------------------------------------------------
# Deterministic engine outcome + combinator
# ---------------------------------------------------------------------

from afritech.platform.core.decision.engine_outcome import (
    EngineOutcome,
)

from afritech.platform.core.decision.combinator import (
    combine,
)

# ---------------------------------------------------------------------
# Public GA ABI (Explicit & Frozen)
# ---------------------------------------------------------------------

__all__ = [
    # Canonical final decision
    "Decision",
    "DecisionVerdict",

    # Explanation primitives
    "DecisionReason",
    "DecisionTrace",

    # Engine outcome + combinator
    "EngineOutcome",
    "combine",
]