from __future__ import annotations
"""
AfriTech Core Registry â€” Engine Catalog (GA-Sealed)

This module defines the canonical list of core decision engines.

RULES:
- Static metadata ONLY
- NO execution
- NO imports of engine implementations
- NO orchestration logic
- NO runtime behavior

This file is consumed by L3 control-plane orchestration.
Changing it is a BREAKING ARCHITECTURAL DECISION.
"""


# ---------------------------------------------------------------------
# Canonical decision engine names
# ---------------------------------------------------------------------
# These are symbolic identifiers only.
# They deliberately do NOT reference concrete classes or modules.
# ---------------------------------------------------------------------

ENGINE_NAMES: tuple[str, ...] = (
    "rbac",       # Capability (can you ever?)
    "policy",     # Conditional rules (should you now?)
    "quota",      # Resource pressure (can you again?)
    "risk",       # Exposure (how dangerous?)
    "consent",    # Legality (are we allowed?)
    "audit",      # Explainability (what happened & why?)
)


# ---------------------------------------------------------------------
# Engine classification helpers (metadata only)
# ---------------------------------------------------------------------

DECISION_ENGINES: frozenset[str] = frozenset(ENGINE_NAMES)

HARD_DENY_ENGINES: frozenset[str] = frozenset((
    "rbac",
    "policy",
    "quota",
    "consent",
))

SOFT_SIGNAL_ENGINES: frozenset[str] = frozenset((
    "risk",
))

OBSERVATION_ENGINES: frozenset[str] = frozenset((
    "audit",
))


# ---------------------------------------------------------------------
# Registry invariants (must hold forever)
# ---------------------------------------------------------------------

assert DECISION_ENGINES == frozenset(ENGINE_NAMES), (
    "ENGINE_NAMES and DECISION_ENGINES must remain consistent"
)


# ---------------------------------------------------------------------
# Public ABI
# ---------------------------------------------------------------------

__all__ = [
    "ENGINE_NAMES",
    "DECISION_ENGINES",
    "HARD_DENY_ENGINES",
    "SOFT_SIGNAL_ENGINES",
    "OBSERVATION_ENGINES",
]
