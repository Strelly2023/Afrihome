#!/usr/bin/env python3
from __future__ import annotations

"""
AfriTech Utility — fix_future_imports
====================================

Normalize or remove `from __future__ import annotations`
across a Python codebase.

Modes:
- remove : delete all occurrences (recommended for Python >= 3.11)
- move   : ensure it appears immediately after the module docstring
           (PEP 236 / PEP 257 compliant)

Features:
- Safe dry-run mode (no file writes)
- Skips virtualenvs and site-packages
- Preserves shebangs, encoding headers, and trailing newlines
- Idempotent and pre-commit friendly
"""

import argparse
from pathlib import Path
from typing import Iterable

# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------

FUTURE_LINE = "from __future__ import annotations"

SKIP_DIRS = {
    "venv",
    ".venv",
    ".tox",
    "site-packages",
    "__pycache__",
}

ENCODING_PREFIXES = ("# -*- coding:", "# coding:")

# ---------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------

def should_skip(path: Path) -> bool:
    return any(part in SKIP_DIRS for part in path.parts)


def find_future_imports(lines: list[str]) -> list[int]:
    return [i for i, ln in enumerate(lines) if ln.strip() == FUTURE_LINE]


def find_insertion_point(lines: list[str]) -> int:
    i = 0

    # Shebang
    if i < len(lines) and lines[i].startswith("#!"):
        i += 1

    # Encoding declaration(s)
    while i < len(lines) and any(lines[i].startswith(pfx) for pfx in ENCODING_PREFIXES):
        i += 1

    # Module docstring
    if i < len(lines) and lines[i].lstrip().startswith(('"""', "'''")):
        quote = lines[i].lstrip()[:3]

        # Single-line docstring
        if lines[i].count(quote) >= 2:
            return i + 1

        # Multi-line docstring
        i += 1
        while i < len(lines):
            if quote in lines[i]:
                return i + 1
            i += 1

    return i


def write_if_changed(path: Path, original: str, updated: str) -> bool:
    if original == updated:
        return False
    path.write_text(updated, encoding="utf-8")
    return True

# ---------------------------------------------------------------------
# Core logic
# ---------------------------------------------------------------------

def fix_file(path: Path, *, mode: str, dry_run: bool) -> bool:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    had_trailing_newline = text.endswith("\n")

    idxs = find_future_imports(lines)
    if not idxs:
        return False

    new_lines = list(lines)

    # Remove all existing future imports
    for idx in reversed(idxs):
        del new_lines[idx]

    if mode == "move":
        insert_at = find_insertion_point(new_lines)
        new_lines.insert(insert_at, FUTURE_LINE)

        if (
            insert_at + 1 < len(new_lines)
            and new_lines[insert_at + 1].strip() != ""
        ):
            new_lines.insert(insert_at + 1, "")

    elif mode != "remove":
        raise ValueError(f"Unsupported mode: {mode}")

    updated = "\n".join(new_lines)
    if had_trailing_newline:
        updated += "\n"

    if dry_run:
        return True

    return write_if_changed(path, text, updated)

# ---------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------

def iter_python_files(root: Path) -> Iterable[Path]:
    for path in root.rglob("*.py"):
        if not should_skip(path):
            yield path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Normalize or remove future annotations imports."
    )
    parser.add_argument(
        "--mode",
        choices=("remove", "move"),
        default="remove",
        help="remove (Py>=3.11) or move below module docstring",
    )
    parser.add_argument("--dry-run", action="store_true", help="Do not write files")
    parser.add_argument("--root", default=".", help="Project root")

    args = parser.parse_args()
    root = Path(args.root)

    changed = 0
    for py_file in iter_python_files(root):
        if fix_file(py_file, mode=args.mode, dry_run=args.dry_run):
            label = "[DRY] would fix" if args.dry_run else "fixed"
            print(f"{label}: {py_file}")
            changed += 1

    suffix = "would be " if args.dry_run else ""
    print(f"\n{changed} file(s) {suffix}fixed.")


if __name__ == "__main__":
    main()