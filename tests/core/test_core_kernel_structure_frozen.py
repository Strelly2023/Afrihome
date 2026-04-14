"""
GA Core â€” Kernel Structure Freeze
--------------------------------

Purpose:
- Prevent adding new files to the kernel without explicit approval
"""

from pathlib import Path

KERNEL_PATH = Path("afritech/platform/core/kernel")


def test_kernel_file_set_frozen():
    expected = sorted([
        "__init__.py",
        "freeze.py",
        "invariants.py",
        "sealed.py",
    ])

    actual = sorted(
        p.name for p in KERNEL_PATH.iterdir()
        if p.is_file()
    )

    assert actual == expected
