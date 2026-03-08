"""
GA Enterprise Core — Kernel Authority

LAYER: L0
Purpose:
- Global freeze control
- Kernel invariant enforcement
"""

from .freeze import (
    assert_kernel_mutable,
    freeze_kernel,
    is_kernel_frozen,
)
from .invariants import (
    assert_invariant,
    assert_not_none,
    assert_true,
)

__all__ = [
    "freeze_kernel",
    "is_kernel_frozen",
    "assert_kernel_mutable",
    "assert_invariant",
    "assert_not_none",
    "assert_true",
]
