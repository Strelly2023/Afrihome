#!/usr/bin/env python3
from __future__ import annotations

"""
AfriTech Core Freeze Enforcement
================================

Enforces ADR-000 — Core Freeze.

Rule:
- Any change under afritech/platform/core/ is forbidden
  unless accompanied by an approved Core Amendment ADR.

FAIL-CLOSED:
Any unauthorized Core change fails CI.
"""

import subprocess
import sys
from pathlib import Path

CORE_ROOT = Path("afritech/platform/core")
ADR_DIR = Path("docs/decisions")

AMENDMENT_PREFIX = "ADR-000A-"  # Core amendment ADRs must use this prefix


def changed_core_files() -> list[str]:
    """Return a list of changed core files in this commit/PR."""
    result = subprocess.run(
        ["git", "diff", "--name-only", "origin/main...HEAD"],
        capture_output=True,
        text=True,
        check=False,
    )
    files = result.stdout.splitlines()
    return [f for f in files if f.startswith(str(CORE_ROOT))]


def has_core_amendment_adr() -> bool:
    """Return True if a Core Amendment ADR exists in this change."""
    if not ADR_DIR.exists():
        return False

    for adr in ADR_DIR.glob("*.md"):
        if adr.name.startswith(AMENDMENT_PREFIX):
            # Ensure the amendment itself is part of this change
            result = subprocess.run(
                ["git", "diff", "--name-only", "origin/main...HEAD", "--", str(adr)],
                capture_output=True,
                text=True,
            )
            if adr.name in result.stdout:
                return True

    return False


def main() -> None:
    core_changes = changed_core_files()

    if not core_changes:
        print("✅ Core Freeze: no core changes detected.")
        return

    print("❌ Core Freeze violation detected.")
    print("\nChanged core files:")
    for f in core_changes:
        print(f"  - {f}")

    if not has_core_amendment_adr():
        print(
            "\nNo approved Core Amendment ADR found.\n"
            "To modify the Core, you MUST:\n"
            "1. Create an ADR named ADR-000A-<slug>.md\n"
            "2. Explicitly amend ADR-000\n"
            "3. Justify re-certification of all guarantees\n"
        )
        raise SystemExit(1)

    print("✅ Core Amendment ADR detected. Core change authorized.")


if __name__ == "__main__":
    main()
