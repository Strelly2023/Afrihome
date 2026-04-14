#!/usr/bin/env python3
from __future__ import annotations

"""
AfriTech HTML Entity Normalizer
===============================

Normalizes HTML-escaped entities that corrupt Python source readability
(e.g. ->, <, >, quotes) while strictly avoiding modification of real HTML.

Modes:
- Fix mode (default): rewrites files deterministically
- Check mode (--check): detects violations and FAILS without modifying files

Enforces: ADR-TV-003 — Source HTML Entity Normalization
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Iterable

# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------

SKIP_DIRS = {"venv", ".venv", ".tox", "site-packages", ".git", "__pycache__"}
EXTS = {".py"}

# High-confidence code-context patterns (HTML-encoded -> decoded)
PATTERNS = [
    # return type annotation
    (re.compile(r"\)\s*-\&gt;\s*"), ") -> "),
    (re.compile(r"([^\S\r\n]|:)\s*-\&gt;\s*"), r"\1 -> "),
    # comparisons
    (re.compile(r"\s+\&lt;\s+"), " < "),
    (re.compile(r"\s+\&gt;\s+"), " > "),
]

# Lines that clearly look like HTML/templates (never touch quotes there)
HTMLY = re.compile(r"&lt;(/|div|span|p|h[1-6]|!--)")

QUOTE_FIXES = [
    (re.compile(r"&quot;"), '"'),
    (re.compile(r"&#39;"), "'"),
]

# ---------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------

def should_skip(path: Path) -> bool:
    return any(part in SKIP_DIRS for part in path.parts)


def iter_python_files(root: Path) -> Iterable[Path]:
    yield from root.rglob("*.py")


def fix_line(line: str) -> str:
    """
    Apply safe, context-aware normalization to a single line.
    """
    # Always allow arrow and comparison fixes,
    # even if the line looks HTML-ish
    for pat, repl in PATTERNS:
        line = pat.sub(repl, line)

    # Skip quote fixes on obvious HTML/template lines
    if HTMLY.search(line):
        return line

    # Conservative quote fixes in Python-looking lines only
    if re.search(
        r"\b(def|class)\b|:\s*(dict|list|set)\[|->|=\s*{|^\s*\w+\s*:",
        line,
    ):
        for pat, repl in QUOTE_FIXES:
            line = pat.sub(repl, line)

    return line


def process_file(path: Path, check_only: bool) -> bool:
    """
    Returns True if changes were needed (or made).
    In --check mode: does NOT write.
    """
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=False)

    new_lines = []
    changed = False

    for ln in lines:
        fixed = fix_line(ln)
        if fixed != ln:
            changed = True
        new_lines.append(fixed)

    if changed and not check_only:
        path.write_text(
            "\n".join(new_lines) + ("\n" if text.endswith("\n") else ""),
            encoding="utf-8",
        )

    return changed


# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Normalize HTML-encoded syntax in AfriTech Python source."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Detect violations only; do not modify files.",
    )

    args = parser.parse_args()
    check_only = args.check

    violations: list[Path] = []
    fixed_count = 0

    for p in iter_python_files(Path(".")):
        if p.is_dir() or should_skip(p) or p.suffix not in EXTS:
            continue

        try:
            changed = process_file(p, check_only=check_only)
            if changed:
                if check_only:
                    violations.append(p)
                else:
                    print(f"fixed: {p}")
                    fixed_count += 1
        except Exception as e:
            print(f"skip (error): {p} -> {e}")

    if check_only:
        if violations:
            print("\n❌ HTML entity violations detected:")
            for p in violations:
                print(f"  {p}")
            print(f"\nTotal violating files: {len(violations)}")
            raise SystemExit(1)
        print("✅ HTML entity check passed.")
    else:
        print(f"\n✅ {fixed_count} file(s) normalized.")


if __name__ == "__main__":
    main()
