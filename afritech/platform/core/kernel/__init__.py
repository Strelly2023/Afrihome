"""
GA Enterprise Core â€” Kernel Authority
------------------------------------

LAYER: L0 (Kernel)
Deterministic: YES
Side effects: NONE

Purpose:
- Global freeze control
- Kernel invariant enforcement

RULE:
- This file defines the FULL Kernel ABI
- Any change here is a BREAKING CHANGE
"""

from .freeze import (
    FREEZE_SENTINEL,
    freeze_kernel,
    is_kernel_frozen,
    assert_kernel_not_frozen,
)

from .invariants import (
    assert_invariant,
    assert_not_none,
    assert_true,
)

from .sealed import (
    assert_kernel_sealed,
)

__all__ = [
    # Freeze control
    "FREEZE_SENTINEL",
    "freeze_kernel",
    "is_kernel_frozen",
    "assert_kernel_not_frozen",

    # Invariants
    "assert_invariant",
    "assert_not_none",
    "assert_true",

    # GA sealing
    "assert_kernel_sealed",
]
