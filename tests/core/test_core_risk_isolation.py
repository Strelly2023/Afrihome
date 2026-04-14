"""
GA Core â€” Risk Isolation Tests
-----------------------------

Purpose:
- Enforce core.risk (L2) isolation rules
- Prevent upward or sideways dependencies
- Guarantee risk remains a pure, deterministic engine

RULES:
- risk MUST NOT import Kernel (L0)
- risk MUST NOT import semantic L1 foundations
- risk MUST NOT import other L2 engines
- risk MAY import core.errors and core.typing (structural utilities)
"""

from pathlib import Path

from tests.core.utils import extract_full_imports

CORE_PATH = Path("afritech/platform/core")
RISK_PATH = CORE_PATH / "risk"

# Forbidden core modules for Risk (L2)
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
    "quota",      # other L2 engine
    # NOTE:
    # core.errors and core.typing are explicitly allowed
}


def test_risk_import_isolation():
    """
    Enforce strict Risk (L2) import boundaries.
    """
    assert RISK_PATH.exists(), "core/risk directory is missing"

    violations = {}

    for py_file in RISK_PATH.rglob("*.py"):
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
        "Risk isolation violations detected:\n"
        + "\n".join(
            f"- {path}: imports forbidden core modules {modules}"
            for path, modules in violations.items()
        )
    )
