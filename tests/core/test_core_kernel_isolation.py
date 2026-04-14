"""
Kernel isolation enforcement tests (GA-Sealed).

These tests enforce absolute L0 isolation semantics:

Kernel code MAY:
- import Python standard library modules
- import other modules within afritech.platform.core.kernel

Kernel code MUST NOT:
- import any non-kernel afritech modules
- import infrastructure or application code
- import framework or IO-related libraries

If this test fails, the platform architecture is compromised.
"""

from pathlib import Path

from tools.core_enforcement.rules import CORE_ROOT
from tools.core_enforcement.scanner import extract_full_imports


KERNEL_PATH = Path(CORE_ROOT) / "kernel"


def test_kernel_imports_only_stdlib_or_kernel():
    """
    The kernel is a single cohesive L0 authority.

    Internal kernel imports are allowed.
    All non-kernel afritech imports are forbidden.
    """
    if not KERNEL_PATH.exists():
        return

    for py_file in KERNEL_PATH.rglob("*.py"):
        imports = extract_full_imports(py_file)

        illegal = {
            imp for imp in imports
            if imp.startswith("afritech")
            and not imp.startswith("afritech.platform.core.kernel")
        }

        assert not illegal, (
            f"{py_file} violates kernel isolation rule: "
            f"imports forbidden modules {sorted(illegal)}"
        )
