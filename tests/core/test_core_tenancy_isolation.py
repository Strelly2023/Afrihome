"""
GA Core â€” Tenancy Isolation Tests
================================

Purpose:
- Enforce strict isolation of core.tenancy (L1 â€” Foundation)
- Prevent upward or sideways dependencies
- Guarantee tenancy remains grammarâ€‘only and deterministic

RULES:
- tenancy MUST NOT import Kernel (L0)
- tenancy MUST NOT import Context, RBAC, Policy, Risk, Quota, Consent, Audit
- tenancy MUST NOT perform resolution, lookup, or registry access
- tenancy MAY import itself, typing, and errors (structural only)

Any failure in this file is a GAâ€‘blocking architectural violation.
"""

from pathlib import Path

from tests.core.utils import extract_full_imports


CORE_PATH = Path("afritech/platform/core")
TENANCY_PATH = CORE_PATH / "tenancy"


# =============================================================
# Forbidden core dependencies for Tenancy (L1)
# =============================================================

FORBIDDEN_CORE_MODULES = {
    # L0
    "kernel",

    # Other L1 foundations not allowed
    "context",
    "identity",
    "time",

    # L2+ engines
    "rbac",
    "policy",
    "quota",
    "risk",
    "consent",
    "audit",
    "decision",
    "governance",
    "registry",
    "events",
    "contracts",
}


# =============================================================
# Isolation test
# =============================================================

def test_tenancy_import_isolation():
    """
    Enforce strict import boundaries for core.tenancy.

    NOTE:
    - core.tenancy is allowed to import itself (intraâ€‘module imports)
    """
    assert TENANCY_PATH.exists(), "core/tenancy directory is missing"

    violations = {}

    for py_file in TENANCY_PATH.rglob("*.py"):
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

            # âœ… Allowed:
            # - selfâ€‘imports (tenancy â†’ tenancy)
            # - typing and errors (L1 utilities)
            if imported_module in {"tenancy", "typing", "errors"}:
                continue

            if imported_module in FORBIDDEN_CORE_MODULES:
                illegal.add(imported_module)

        if illegal:
            violations[str(py_file)] = sorted(illegal)

    assert not violations, (
        "Tenancy isolation violations detected:\n"
        + "\n".join(
            f"- {path} imports forbidden core modules {modules}"
            for path, modules in violations.items()
        )
    )
