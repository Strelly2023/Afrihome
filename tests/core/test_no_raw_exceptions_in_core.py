"""
GA Core â€” Raw Exception Guard (GA-Sealed)

Purpose:
- Enforce the unified deterministic error strategy in afritech.platform.core
- Prevent reintroduction of RuntimeError / Exception after GA hardening

RULE:
- NO use of:
    - raise RuntimeError
    - raise Exception(...)
  anywhere in afritech.platform.core
  EXCEPT inside core/kernel/

RATIONALE:
- All core (L1/L2) errors MUST derive from CoreError
- Structural failures MUST be explicit and typed
- Decisions MUST NOT be represented by exceptions
- Kernel (L0) is explicitly exempt from CoreError constraints

This test is ARCHITECTURAL LAW.
Any failure here is a BREAKING CHANGE and requires an ADR.
"""

from pathlib import Path


CORE_ROOT = Path("afritech/platform/core")
KERNEL_ROOT = CORE_ROOT / "kernel"

FORBIDDEN_PATTERNS = (
    "raise RuntimeError",
    "raise Exception(",
)


def test_no_raw_exceptions_in_core():
    """
    Enforce that no raw RuntimeError or Exception is raised anywhere
    in afritech.platform.core outside the kernel.
    """
    assert CORE_ROOT.exists(), "afritech/platform/core not found"

    violations: list[str] = []

    for py_file in CORE_ROOT.rglob("*.py"):
        # ----------------------------------------------------
        # Kernel is explicitly exempt
        # ----------------------------------------------------
        try:
            if py_file.is_relative_to(KERNEL_ROOT):
                continue
        except AttributeError:
            # Python < 3.9 fallback (defensive)
            if str(py_file).startswith(str(KERNEL_ROOT)):
                continue

        # Skip cache / generated files defensively
        if "__pycache__" in py_file.parts:
            continue

        source = py_file.read_text(encoding="utf-8")

        for pattern in FORBIDDEN_PATTERNS:
            if pattern in source:
                violations.append(
                    f"{py_file}: contains forbidden pattern '{pattern}'"
                )

    if violations:
        message = (
            "Raw RuntimeError / Exception usage detected in core "
            "(GA VIOLATION):\n"
            + "\n".join(violations)
        )
        raise AssertionError(message)
