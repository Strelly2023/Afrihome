"""
GA Enterprise Core â€” Errors Public Interface
--------------------------------------------

This package exposes the canonical, GA-stable error hierarchy
for afritech.platform.core.

Rules:
- All public core errors MUST be exported here
- Kernel compatibility errors are re-exported intentionally
- The kernel (L0) MUST NOT import from this module
"""

from .base import (
    CoreError,
    InvariantViolationError,
    ValidationError,
    GrammarViolationError,
    AuthorizationError,
    TenantIsolationError,
    StrictWriteViolationError,
    IdempotencyViolationError,
)

# Legacy / compatibility export (L1 only)
from .kernel import KernelFrozenError


__all__ = [
    # Base
    "CoreError",

    # Invariants / validation
    "InvariantViolationError",
    "ValidationError",
    "GrammarViolationError",

    # Authorization / governance
    "AuthorizationError",
    "TenantIsolationError",

    # Execution discipline
    "StrictWriteViolationError",
    "IdempotencyViolationError",

    # Kernel compatibility (EXPLICITLY non-kernel)
    "KernelFrozenError",
]
