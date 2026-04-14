"""
GA Core â€” Quota Isolation Tests
------------------------------

Purpose:
- Enforce core.quota (L2) isolation rules
- Prevent upward or sideways dependencies
- Guarantee quota remains a pure, deterministic engine

RULES:
- quota MUST NOT import Kernel (L0)
- quota MUST NOT import semantic L1 foundations
- quota MUST NOT import other L2 engines
- quota MAY import core.errors and core.typing (structural utilities)
"""

from pathlib import Path

from tests.core.utils import extract_full_imports

CORE_PATH = Path("afritech/platform/core")
QUOTA_PATH = CORE_PATH / "quota"

# Forbidden core modules for Quota (L2)
FORBIDDEN_CORE_MODULES = {
    "kernel",     # L0
    "identity",   # L1 semantic
    "context",    # L1 semantic
    "tenancy",    # L1 semantic
    "time",       # L1 semantic
    "execution",  # control plane
    "rbac",       # other L2 engine
    "policy",     # other L2 engine
    "audit",      # other L2 engine
    # NOTE:
    # core.errors and core.typing are explicitly allowed
}


def test_quota_import_isolation():
    """
    Enforce strict Quota (L2) import boundaries.
    """
    assert QUOTA_PATH.exists(), "core/quota directory is missing"

    violations = {}

    for py_file in QUOTA_PATH.rglob("*.py"):
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
        "Quota isolation violations detected:\n"
        + "\n".join(
            f"- {path}: imports forbidden core modules {modules}"
            for path, modules in violations.items()
        )
    )
