"""
GA Core â€” RBAC Isolation Tests
-----------------------------

Purpose:
- Enforce RBAC (L2) isolation rules
- Prevent upward or sideways dependencies
- Ensure RBAC remains a pure evaluation engine

RULES:
- RBAC MUST NOT import Kernel (L0)
- RBAC MUST NOT import identity / tenancy / context / time
- RBAC MAY import:
    - Python standard library
    - core.typing (types only)
    - core.errors (typed error hierarchy)
    - other RBAC modules
"""

from pathlib import Path

from tests.core.utils import extract_full_imports

CORE_PATH = Path("afritech/platform/core")
RBAC_PATH = CORE_PATH / "rbac"

# Forbidden core modules for RBAC (L2)
FORBIDDEN_CORE_MODULES = {
    "kernel",     # L0
    "identity",   # L1
    "context",    # L1
    "tenancy",    # L1
    "time",       # L1
    # NOTE:
    # core.typing and core.errors are explicitly allowed
}


def test_rbac_import_isolation():
    """
    Enforce strict RBAC import boundaries.

    RBAC is a pure L2 engine and must remain isolated from:
    - Kernel (L0)
    - Identity, tenancy, context, and time foundations
    """
    assert RBAC_PATH.exists(), "core/rbac directory is missing"

    violations = {}

    for py_file in RBAC_PATH.rglob("*.py"):
        imports = extract_full_imports(py_file)

        illegal = set()

        for imp in imports:
            # Ignore stdlib and thirdâ€‘party imports
            if not imp.startswith("afritech"):
                continue

            parts = imp.split(".")

            # Only evaluate imports inside afritech.platform.core
            if "core" not in parts:
                continue

            core_index = parts.index("core")
            try:
                imported_module = parts[core_index + 1]
            except IndexError:
                continue

            if imported_module in FORBIDDEN_CORE_MODULES:
                illegal.add(imported_module)

        if illegal:
            violations[py_file] = sorted(illegal)

    assert not violations, (
        "RBAC isolation violations detected:\n"
        + "\n".join(
            f"- {path}: imports forbidden core modules {modules}"
            for path, modules in violations.items()
        )
    )
