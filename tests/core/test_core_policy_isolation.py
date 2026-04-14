"""
GA Core â€” Policy Isolation Tests
-------------------------------

Purpose:
- Enforce core.policy (L2) isolation rules
- Prevent upward or sideways dependencies
- Guarantee Policy remains a pure, deterministic engine

RULES:
- Policy MUST NOT import Kernel (L0)
- Policy MUST NOT import identity / context / tenancy / time
- Policy MAY import:
    - Python standard library
    - core.typing
    - core.errors
    - core.policy submodules only
"""

from pathlib import Path

from tests.core.utils import extract_full_imports

CORE_PATH = Path("afritech/platform/core")
POLICY_PATH = CORE_PATH / "policy"

# Forbidden core modules for Policy (L2)
FORBIDDEN_CORE_MODULES = {
    "kernel",     # L0
    "identity",   # L1
    "context",    # L1
    "tenancy",    # L1
    "time",       # L1
    # NOTE:
    # core.errors and core.typing are explicitly allowed
}


def test_policy_import_isolation():
    """
    Enforce strict Policy import boundaries.
    """
    assert POLICY_PATH.exists(), "core/policy directory is missing"

    violations = {}

    for py_file in POLICY_PATH.rglob("*.py"):
        imports = extract_full_imports(py_file)
        illegal = set()

        for imp in imports:
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
        "Policy isolation violations detected:\n"
        + "\n".join(
            f"- {path}: imports forbidden core modules {modules}"
            for path, modules in violations.items()
        )
    )
