from __future__ import annotations

"""
GA Core â€” Import Boundary Enforcement Tests
===========================================

These tests enforce the canonical GA import boundaries for
afritech.platform.core.

They ensure that:
- Each core module imports ONLY what the GA contract allows
- Kernel (L0) remains absolutely isolated
- No sideways or upward dependencies are introduced

FAILURE OF ANY TEST IN THIS FILE MEANS:
â†’ CORE ARCHITECTURE HAS BEEN VIOLATED
"""

from pathlib import Path
from typing import Iterable, Optional

from tools.core_enforcement.rules import (
    CORE_IMPORT_RULES,
    CORE_ROOT,
    KERNEL_FORBIDDEN_IMPORT_ROOTS,
)
from tools.core_enforcement.scanner import extract_import_roots


CORE_PATH = Path(CORE_ROOT)


# =============================================================
# Helpers
# =============================================================

def core_module_from_path(py_file: Path) -> Optional[str]:
    """
    Given a Python file path under CORE_ROOT, return the
    top-level core module name.

    Example:
        afritech/platform/core/rbac/engine.py â†’ "rbac"
    """
    try:
        relative = py_file.relative_to(CORE_PATH)
    except ValueError:
        return None

    if not relative.parts:
        return None

    return relative.parts[0]


def iter_core_py_files() -> Iterable[Path]:
    """
    Iterate over all Python files under CORE_ROOT.
    """
    yield from CORE_PATH.rglob("*.py")


# =============================================================
# Core import boundary enforcement
# =============================================================

def test_core_import_boundaries():
    """
    Enforce canonical GA import rules for all core modules.

    Each core module may ONLY import other core modules
    explicitly allowed by CORE_IMPORT_RULES.
    """
    for py_file in iter_core_py_files():
        module = core_module_from_path(py_file)
        if module is None:
            continue

        # Skip __init__.py at the core root only
        if py_file.name == "__init__.py" and py_file.parent == CORE_PATH:
            continue

        if module not in CORE_IMPORT_RULES:
            raise AssertionError(
                f"{py_file} belongs to unknown core module '{module}'. "
                f"This module is not defined in CORE_IMPORT_RULES."
            )

        allowed_core_imports = set(CORE_IMPORT_RULES[module])
        import_roots = extract_import_roots(py_file)

        illegal_imports: set[str] = set()

        for root in import_roots:
            # Only enforce afritech imports
            if not root.startswith("afritech"):
                continue

            parts = root.split(".")
            try:
                core_index = parts.index("core")
                imported_module = parts[core_index + 1]
            except (ValueError, IndexError):
                continue

            if imported_module not in allowed_core_imports:
                illegal_imports.add(imported_module)

        assert not illegal_imports, (
            "âŒ Core import boundary violation detected\n\n"
            f"File: {py_file}\n"
            f"Module: {module}\n"
            f"Illegal imports: {sorted(illegal_imports)}\n"
            f"Allowed imports: {sorted(allowed_core_imports)}\n"
        )


# =============================================================
# Kernel absolute isolation
# =============================================================

def test_kernel_is_absolutely_isolated():
    """
    Kernel (L0) MUST NOT import ANYTHING from afritech.platform.core,
    including errors, typing, or any L1/L2 modules.
    """
    kernel_path = CORE_PATH / "kernel"
    if not kernel_path.exists():
        return

    for py_file in kernel_path.rglob("*.py"):
        import_roots = extract_import_roots(py_file)
        forbidden = import_roots & KERNEL_FORBIDDEN_IMPORT_ROOTS

        assert not forbidden, (
            "âŒ Kernel isolation violation detected\n\n"
            f"File: {py_file}\n"
            f"Forbidden imports: {sorted(forbidden)}\n"
            "Kernel must be absolutely isolated.\n"
        )
