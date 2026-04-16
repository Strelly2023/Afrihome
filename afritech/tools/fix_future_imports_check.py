#!/usr/bin/env python3
from __future__ import annotations

"""
Annotations Guard
==================

Check-only wrapper for fix_future_imports.py.

- Never edits files
- Fails CI if annotations drift is detected
"""

import subprocess
import sys


def main() -> int:
    cmd = [
        sys.executable,
        "tools/fix_future_imports.py",
        "--dry-run",
        "--mode",
        "remove",
    ]

    proc = subprocess.run(cmd, capture_output=True, text=True)

    if proc.returncode != 0:
        print(proc.stdout)
        print(proc.stderr)
        return proc.returncode

    if "would fix:" in proc.stdout:
        print("❌ Future-annotations drift detected.")
        print("   Run: python tools/fix_future_imports.py --mode remove")
        return 1

    print("✅ Future-annotations check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())