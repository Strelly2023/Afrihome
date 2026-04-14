#afritech/platform/core/kernel/sealed.py
"""
GA Enterprise Core â€” GA Seal Enforcement
---------------------------------------

LAYER: L0 (Kernel)
Dependencies: stdlib only (kernel internal)
Deterministic: YES
Side effects: NONE

Purpose:
- Enforce final GA freeze invariant
- Act as the single GA execution gate

Rules:
- Must be called by every process entrypoint
- Must fail hard if the kernel is not frozen
"""

from .freeze import is_kernel_frozen


def assert_kernel_sealed() -> None:
    """
    Final GA assertion.

    Must be called by:
    - application entrypoints
    - worker bootstraps
    - CLI roots

    Raises:
        RuntimeError: if the kernel is not frozen.
    """
    if not is_kernel_frozen():
        raise RuntimeError(
            "GA invariant violated: kernel must be frozen before execution"
        )
__all__ = [
    "assert_kernel_sealed",
]
