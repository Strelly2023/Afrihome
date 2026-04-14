"""
GA Enterprise Core â€” Global Freeze Authority
--------------------------------------------

LAYER: L0 (Kernel)
Dependencies: stdlib only
Deterministic: YES
Threading: NONE
IO: NONE

Rules:
- Freeze is explicit
- Freeze is irreversible
- Freeze is global
- No auto-freeze
- No implicit mutation
"""

from typing import Final


# ============================================================
# Internal freeze state (single source of truth)
# ============================================================

_KERNEL_FROZEN: bool = False

FREEZE_SENTINEL: Final[str] = "GA_KERNEL_FROZEN_V1"


# ============================================================
# Public API
# ============================================================

def freeze_kernel() -> str:
    """
    Irreversibly freeze the kernel.

    Returns:
        Deterministic freeze sentinel for audit / replay.

    Raises:
        RuntimeError: if the kernel is already frozen.
    """
    global _KERNEL_FROZEN

    if _KERNEL_FROZEN:
        raise RuntimeError("Kernel is already frozen")

    _KERNEL_FROZEN = True
    return FREEZE_SENTINEL


def is_kernel_frozen() -> bool:
    """
    Pure read of kernel freeze state.
    """
    return _KERNEL_FROZEN


def assert_kernel_not_frozen() -> None:
    """
    Raises if mutation is attempted after freeze.

    Must be called by:
    - registries
    - grammar authorities
    - policy mutation points
    """
    if _KERNEL_FROZEN:
        raise RuntimeError("Kernel is frozen")
    
__all__ = [
    "FREEZE_SENTINEL",
    "freeze_kernel",
    "is_kernel_frozen",
    "assert_kernel_not_frozen",
]
