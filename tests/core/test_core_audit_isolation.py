"""
GA Core â€” Audit Isolation Tests
------------------------------

Purpose:
- Enforce core.audit (L2) isolation rules
- Prevent upward or sideways dependencies
- Guarantee audit remains a pure, deterministic engine

RULES:
- audit MUST NOT import Kernel (L0)
- audit MUST NOT import semantic L1 foundations
- audit MUST NOT import control plane or infrastructure
- audit MAY import core.errors and core.typing (structural utilities)
"""

from pathlib import Path

from tests.core.utils import extract_full_imports

CORE_PATH = Path("afritech/platform/core")
AUDIT_PATH = CORE_PATH / "audit"

# Forbidden core modules for Audit (L2)
FORBIDDEN_CORE_MODULES = {
    "kernel",     # L0
    "identity",   # L1 semantic
    "context",    # L1 semantic
    "tenancy",    # L1 semantic
    "time",       # L1 semantic
    "execution",  # control plane
    "rbac",       # consumes decisions, not engines
    "policy",    # consumes results, not logic
    # NOTE:
    # core.errors and core.typing are explicitly allowed
}


def test_audit_import_isolation():
    """
    Enforce strict Audit (L2) import boundaries.
    """
    assert AUDIT_PATH.exists(), "core/audit directory is missing"

    violations = {}

    for py_file in AUDIT_PATH.rglob("*.py"):
        imports = extract_full_imports(py_file)
        illegal = set()

        for imp in imports:
            # Ignore stdlib and thirdâ€‘party imports
            if not imp.startswith("afritech"):
                continue

            parts = imp.split(".")
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
        "Audit isolation violations detected:\n"
        + "\n".join(
            f"- {path}: imports forbidden core modules {modules}"
            for path, modules in violations.items()
        )
    )
