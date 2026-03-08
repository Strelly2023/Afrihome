
"""
GA Enterprise Core — Global Freeze Authority
--------------------------------------------

LAYER: L0
Dependencies: core.errors only
Deterministic: YES
Threading: NONE (by design)
IO: NONE

Rules:
- Freeze is irreversible.
- Freeze is global.
- No auto-freeze.
- No implicit mutation.
- Freeze must be explicit.
"""


from typing import Final

from core.errors import KernelFrozenError


# ============================================================
# Internal Freeze State
# ============================================================

_KERNEL_FROZEN: bool = False

FREEZE_SENTINEL: Final[str] = "GA_KERNEL_FROZEN_V1"


# ============================================================
# Public API
# ============================================================

def freeze_kernel() -> str:
    """
    Irreversibly freezes the kernel.

    Returns:
        A deterministic sentinel string for audit purposes.

    Raises:
        KernelFrozenError: if already frozen.
    """
    global _KERNEL_FROZEN

    if _KERNEL_FROZEN:
        raise KernelFrozenError("Kernel is already frozen")

    _KERNEL_FROZEN = True
    return FREEZE_SENTINEL


def is_kernel_frozen() -> bool:
    """
    Returns current freeze state.
    Pure read. No mutation.
    """
    return _KERNEL_FROZEN


def assert_kernel_mutable() -> None:
    """
    Raises if the kernel has been frozen.

    Must be called by:
    - Registries
    - Grammar authorities
    - Policy mutation points
    """
    if _KERNEL_FROZEN:
        raise KernelFrozenError()
