#!/usr/bin/env python3
from __future__ import annotations

"""
AfriTech Core Checksum Enforcement
=================================

Enforces ADR-000 — Core Freeze
via cryptographic checksum comparison.

FAIL-CLOSED:
Any checksum mismatch fails CI unless an approved Core Amendment ADR exists.
"""

import hashlib
import json
import subprocess
from pathlib import Path

CORE_ROOT = Path("afritech/platform/core")
LEDGER = Path("docs/constitution/core_checksums.json")
ADR_DIR = Path("docs/decisions")
AMENDMENT_PREFIX = "ADR-000A-"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()


def core_amendment_present() -> bool:
    if not ADR_DIR.exists():
        return False

    for adr in ADR_DIR.glob(f"{AMENDMENT_PREFIX}*.md"):
        result = subprocess.run(
            ["git", "diff", "--name-only", "origin/main...HEAD", "--", str(adr)],
            capture_output=True,
            text=True,
        )
        if adr.name in result.stdout:
            return True

    return False


def main() -> None:
    if not LEDGER.exists():
        raise SystemExit("❌ Core checksum ledger missing.")

    data = json.loads(LEDGER.read_text(encoding="utf-8"))
    expected = data["files"]

    violations: list[str] = []

    for rel_path, expected_hash in expected.items():
        path = Path(rel_path)
        if not path.exists():
            violations.append(f"Missing core file: {rel_path}")
            continue

        actual = sha256(path)
        if actual != expected_hash:
            violations.append(f"Checksum mismatch: {rel_path}")

    if violations:
        if core_amendment_present():
            print("⚠️ Core checksum mismatch detected, but Core Amendment ADR present.")
            return

        print("❌ Core Freeze violation (checksum mismatch):\n")
        for v in violations:
            print(f"  - {v}")
        print(
            "\nTo modify the Core you MUST:\n"
            "1. Add an ADR-000A-*.md Core Amendment\n"
            "2. Regenerate core_checksums.json\n"
            "3. Re-certify all Core guarantees\n"
        )
        raise SystemExit(1)

    print("✅ Core checksum ledger verified — Core integrity intact.")


if __name__ == "__main__":
    main()
