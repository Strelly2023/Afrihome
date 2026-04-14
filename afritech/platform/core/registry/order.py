from __future__ import annotations
"""
AfriTech Core Registry â€” Decision Order (GA-Sealed)

This module defines the canonical, immutable execution order
of core decision engines.

RULES:
- Static metadata ONLY
- NO execution
- NO imports of engine implementations
- NO orchestration logic
- NO control flow
- Deterministic and replay-safe

This file is consumed by L3 control-plane orchestration.
Any change is a BREAKING ARCHITECTURAL DECISION.
"""


# ---------------------------------------------------------------------
# Canonical decision pipeline order
# ---------------------------------------------------------------------
# The order reflects deny-wins decision semantics:
#
#   1. Capability (RBAC)
#   2. Conditional rules (Policy)
#   3. Resource pressure (Quota)
#   4. Risk scoring (Risk)
#   5. Legal permission (Consent)
#   6. Explainability (Audit)
#
# NOTE:
# - Engines earlier in the sequence may short-circuit execution.
# - Later engines MUST NOT affect allow/deny outcome if an earlier
#   hard-deny occurs.
# ---------------------------------------------------------------------

DECISION_ORDER: tuple[str, ...] = (
    "rbac",
    "policy",
    "quota",
    "risk",
    "consent",
    "audit",
)


# ---------------------------------------------------------------------
# Order invariants (must hold forever)
# ---------------------------------------------------------------------

# Hard-deny engines must always precede audit
assert DECISION_ORDER[-1] == "audit", (
    "Audit must be last in DECISION_ORDER"
)

# RBAC must always be first (capability gate)
assert DECISION_ORDER[0] == "rbac", (
    "RBAC must be first in DECISION_ORDER"
)


# ---------------------------------------------------------------------
# Public ABI
# ---------------------------------------------------------------------

__all__ = [
    "DECISION_ORDER",
]
