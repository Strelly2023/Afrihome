from __future__ import annotations

"""
AfriTech Core Governance â€” Evaluation Helpers (GA-Sealed)

This module provides pure, deterministic helper functions for
interpreting governance declarations (rules and constraints).

These helpers:
- DO NOT enforce anything
- DO NOT perform side effects
- DO NOT evaluate engine logic
- DO NOT access runtime state

They exist solely to support higher layers (e.g. control_plane)
in making lawful enforcement decisions.

Any change requires an ADR.
"""

from afritech.platform.core.governance.regimes import GovernanceRegime
from afritech.platform.core.decision.decision import DecisionVerdict


# ============================================================================
# Governance Interpretation Helpers (Pure)
# ============================================================================

def is_override_allowed(
    *,
    verdict: DecisionVerdict,
    regime: GovernanceRegime,
) -> bool:
    """
    Determine whether a decision MAY be overridden under
    the given governance regime.

    This function is:
    - Pure
    - Deterministic
    - Referentially transparent

    It does NOT:
    - enforce the decision
    - override the decision
    - interpret policy logic
    - access runtime state

    Interpretation rule (constitutional):

    - A DENY verdict is non-overrideable if ANY constraint in the
      active governance regime declares itself non-overrideable.
    """

    if verdict is DecisionVerdict.DENY:
        for constraint in regime.constraints:
            if constraint.constraint_id.endswith(".non_overrideable"):
                return False

    return True
