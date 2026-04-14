from __future__ import annotations
"""
GA Enterprise Core â€” Kernel Error Compatibility Layer
-----------------------------------------------------

LAYER: L1 (Foundation)
Dependencies: core.errors.base, stdlib only
Deterministic: YES
Side effects: NONE

Purpose:
- Preserve backward compatibility for legacy imports
- Bridge historical kernel error references to the new GA error system

IMPORTANT:
- The kernel (L0) MUST NOT import this module
- This module exists ONLY to support transitional callers
- New code SHOULD NOT import from core.errors.kernel
"""



from .base import (
    InvariantViolationError,
    GrammarViolationError,
    AuthorizationError,
)


# ============================================================
# Kernel Compatibility Error
# ============================================================

class KernelFrozenError(RuntimeError):
    """
    Raised when mutation is attempted on a frozen kernel.

    NOTE:
    - This error exists ONLY for legacy compatibility
    - The kernel itself raises RuntimeError directly
    - New core code MUST NOT depend on this type
    """
    pass


# ============================================================
# Public Compatibility Surface
# ============================================================

__all__ = [
    "KernelFrozenError",
    "InvariantViolationError",
    "GrammarViolationError",
    "AuthorizationError",
]
