#!/usr/bin/env python3
from __future__ import annotations

"""
AfriTech Future Import Validator
================================

Enforces strict placement of `from __future__ import ...` statements.

Constitutional Rationale:
- Future imports alter parsing semantics.
- They must be visible immediately to any reader or tool.
- Delayed future imports introduce semantic ambiguity and drift.

Rule:
- Any `from __future__ import ...` MUST appear:
  - at the top of the file, OR
  - immediately after a module docstring.
- Any future import appearing later is a violation.

This tool is FAIL-CLOSED:
- Any violation must fail CI.
"""

from pathlib import Path
from typing import Iterable

# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------

SKIP_DIRS = {
    "venv",
    ".venv",
    ".tox",
    "site-packages",
    "__pycache__",
}

MAX_ALLOWED_LINE = 20  # generous, but bounded


# ---------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------

def should_skip(path: Path) -> bool:
    """Return True if the path should be ignored."""
    return any(part in SKIP_DIRS for part in path.parts)


def read_lines(path: Path) -> list[str]:
    """Safely read UTF-8 source lines."""
    return path.read_text(encoding="utf-8").splitlines()


def first_non_empty_non_comment(lines: list[str]) -> int | None:
    """
    Return the index (0-based) of the first non-empty, non-comment line.
    """
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            return i
    return None


def find_future_imports(lines: list[str]) -> list[int]:
    """
    Return a list of line numbers (1-based)
    where `from __future__ import` appears.
    """
    return [
        i + 1
        for i, line in enumerate(lines)
        if line.lstrip().startswith("from __future__ import")
    ]


def validate_future_import_order(path: Path) -> list[str]:
    """
    Validate future import placement in a file.

    Returns a list of human-readable violation messages.
    """
    violations: list[str] = []
    lines = read_lines(path)

    if not lines:
        return violations

    future_lines = find_future_imports(lines)
    if not future_lines:
        return violations

    # Determine the allowed region
    first_code_line = first_non_empty_non_comment(lines)
    if first_code_line is None:
        return violations

    # Support module-level docstring
    allowed_start = first_code_line + 1
    if lines[first_code_line].lstrip().startswith(('"""', "'''")):
        # Walk until end of docstring
        for i in range(first_code_line + 1, len(lines)):
            if lines[i].rstrip().endswith(('"""', "'''")):
                allowed_start = i + 2
                break

    for line_no in future_lines:
        if line_no > allowed_start or line_no > MAX_ALLOWED_LINE:
            violations.append(
                f"{path}:{line_no} — future import must appear at top of file"
            )

    return violations


# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------

def iter_python_files(root: Path) -> Iterable[Path]:
    """Yield all Python source files under root."""
    yield from root.rglob("*.py")


def main() -> None:
    violations: list[str] = []

    for py in iter_python_files(Path(".")):
        if should_skip(py):
            continue
        violations.extend(validate_future_import_order(py))

    if violations:
        print("❌ Future import placement violations detected:\n")
        for v in sorted(violations):
            print(f"  {v}")
        print(f"\nTotal violations: {len(violations)}")
        raise SystemExit(1)

    print("✅ Future import placement check passed.")


if __name__ == "__main__":
    main()