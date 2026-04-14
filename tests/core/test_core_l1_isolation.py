"""
L1 (Core Foundations) isolation enforcement tests (GA-Sealed).

These tests enforce that L1 modules:
- depend only on kernel, themselves, or explicitly allowed L1 modules
- never depend on L2 engines or L3 composition
- remain pure foundational building blocks
"""

from pathlib import Path

from tools.core_enforcement.rules import CORE_ROOT, CORE_IMPORT_RULES
from tools.core_enforcement.scanner import extract_full_imports


CORE_PATH = Path(CORE_ROOT)

L1_MODULES = {
    "errors",
    "typing",
    "time",
    "identity",
    "context",
    "tenancy",
}


def test_l1_import_boundaries():
    """
    Enforce canonical GA import rules for all L1 modules.
    """
    for module in L1_MODULES:
        module_path = CORE_PATH / module
        if not module_path.exists():
            continue

        # Allowed:
        # - self
        # - kernel
        # - explicitly listed dependencies
        allowed = set(CORE_IMPORT_RULES.get(module, [])) | {
            module,
            "kernel",
        }

        for py_file in module_path.rglob("*.py"):
            imports = extract_full_imports(py_file)

            illegal = set()

            for imp in imports:
                if not imp.startswith("afritech"):
                    continue

                parts = imp.split(".")
                try:
                    core_index = parts.index("core")
                    imported_module = parts[core_index + 1]
                except (ValueError, IndexError):
                    continue

                if imported_module not in allowed:
                    illegal.add(imported_module)

            assert not illegal, (
                f"{py_file} violates L1 isolation: "
                f"imports forbidden core modules {sorted(illegal)} "
                f"(allowed: {sorted(allowed)})"
            )
