from __future__ import annotations
#afritech/platform/core/registry/invariants.py
"""
AfriTech Core Registry â€” Architectural Invariants (GA-Sealed)

This module defines immutable invariants that describe
the fundamental, non-negotiable properties of the core
decision architecture.

RULES:
- Declarative metadata ONLY
- NO execution
- NO control flow
- NO imports of engine implementations
- NO runtime behavior

Changing ANY value in this file requires an ADR.
"""



# ---------------------------------------------------------------------
# Core decision system invariants
# ---------------------------------------------------------------------
# These properties define WHAT the core guarantees,
# not HOW it is implemented.
# ---------------------------------------------------------------------

# All core decision engines MUST be deterministic
REQUIRES_DETERMINISM: bool = True

# All core decision engines MUST be replay-safe
# (same inputs => same outputs forever)
REQUIRES_REPLAY_SAFETY: bool = True

# Authorization semantics are deny-wins
# (any hard deny short-circuits the pipeline)
DENY_WINS: bool = True


# ---------------------------------------------------------------------
# Purity and side-effect invariants
# ---------------------------------------------------------------------

# Core engines MUST NOT perform IO
NO_IO_ALLOWED: bool = True

# Core engines MUST NOT access clocks directly
# Time may only enter the core as injected data
NO_DIRECT_TIME_ACCESS: bool = True

# Core engines MUST NOT persist data
NO_PERSISTENCE: bool = True

# Core engines MUST NOT perform orchestration
NO_ORCHESTRATION: bool = True


# ---------------------------------------------------------------------
# Layering invariants
# ---------------------------------------------------------------------

# Core L2 engines must never depend on control-plane code
NO_CONTROL_PLANE_DEPENDENCY: bool = True

# Core must never depend on infrastructure
NO_INFRASTRUCTURE_DEPENDENCY: bool = True

# Kernel is absolutely isolated
KERNEL_IS_ABSOLUTE: bool = True


# ---------------------------------------------------------------------
# Registry intent invariant
# ---------------------------------------------------------------------

# Registry exists solely for static wiring metadata
REGISTRY_IS_STATIC: bool = True


# ---------------------------------------------------------------------
# Public ABI
# ---------------------------------------------------------------------

__all__ = [
    # Decision semantics
    "REQUIRES_DETERMINISM",
    "REQUIRES_REPLAY_SAFETY",
    "DENY_WINS",

    # Purity rules
    "NO_IO_ALLOWED",
    "NO_DIRECT_TIME_ACCESS",
    "NO_PERSISTENCE",
    "NO_ORCHESTRATION",

    # Layering rules
    "NO_CONTROL_PLANE_DEPENDENCY",
    "NO_INFRASTRUCTURE_DEPENDENCY",
    "KERNEL_IS_ABSOLUTE",

    # Registry rule
    "REGISTRY_IS_STATIC",
]
