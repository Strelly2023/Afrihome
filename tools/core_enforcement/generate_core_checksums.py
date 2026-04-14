#!/usr/bin/env python3
from __future__ import annotations

"""
AfriTech Core Checksum Generator
================================

Generates the canonical checksum ledger for the Core.

This tool MUST be run only:
- during initial Core ratification
- during an approved Core amendment (ADR-000A)

It is NOT run automatically in CI.
"""

import hashlib
import json
from pathlib import Path
from datetime import datetime, timezone

CORE_ROOT = Path("afritech/platform/core")
OUTPUT = Path("docs/constitution/core_checksums.json")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    if not CORE_ROOT.exists():
        raise SystemExit("Core root does not exist.")

    files = {}
    for p in sorted(CORE_ROOT.rglob("*.py")):
        if p.is_file():
            files[p.as_posix()] = sha256(p)

    ledger = {
        "schema_version": 1,
        "core_root": CORE_ROOT.as_posix(),
        "hash_algorithm": "sha256",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "files": files,
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(ledger, indent=2) + "\n", encoding="utf-8")

    print(f"✅ Core checksum ledger written to {OUTPUT}")
    print(f"Tracked files: {len(files)}")


if __name__ == "__main__":
    main()