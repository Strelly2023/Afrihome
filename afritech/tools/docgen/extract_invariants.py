#!/usr/bin/env python3
from __future__ import annotations
# tools/docgen/extract_invariants.py
"""
Invariant Documentation Generator
=================================

This script extracts **semantic invariants** from executable tests and
renders them as authoritative documentation.

SOURCE OF TRUTH:
- tests ARE the law
- documentation is a derived artifact

Do NOT edit generated files manually.

Usage:
    python tools/docgen/extract_invariants.py

Output:
    docs/generated/invariants.md
"""

from pathlib import Path
import ast
from dataclasses import dataclass
from typing import List


# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------

TEST_ROOT = Path("tests/core")
OUTPUT_FILE = Path("docs/generated/invariants.md")

INVARIANT_TEST_SUFFIX = "invariants.py"


# ---------------------------------------------------------------------
# Model
# ---------------------------------------------------------------------

@dataclass(frozen=True)
class Invariant:
    """A single semantic invariant extracted from a test."""
    name: str
    description: str
    source_file: str


# ---------------------------------------------------------------------
# Extraction logic
# ---------------------------------------------------------------------

def extract_invariants() -> List[Invariant]:
    """
    Parse invariant tests and extract invariant descriptions.

    An invariant is defined as:
    - a function named `test_*`
    - located in a file ending with `*invariants.py`
    - optionally documented with a docstring
    """

    invariants: List[Invariant] = []

    for test_file in TEST_ROOT.glob(f"test_*{INVARIANT_TEST_SUFFIX}"):
        tree = ast.parse(
            test_file.read_text(encoding="utf-8"),
            filename=str(test_file),
        )

        for node in tree.body:
            if not isinstance(node, ast.FunctionDef):
                continue

            if not node.name.startswith("test_"):
                continue

            docstring = ast.get_docstring(node)
            description = (
                docstring.strip()
                if docstring
                else "_No explicit description provided._"
            )

            invariants.append(
                Invariant(
                    name=node.name,
                    description=description,
                    source_file=test_file.name,
                )
            )

    return sorted(invariants, key=lambda i: i.name)


# ---------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------

def render_markdown(invariants: List[Invariant]) -> str:
    """
    Render invariants into a Markdown document.

    The document is intentionally read‑only and declarative.
    """

    lines: list[str] = [
        "# Core Decision System — Semantic Invariants",
        "",
        "> ⚠️ **GENERATED FILE — DO NOT EDIT**",
        ">",
        "> This document is generated directly from executable tests.",
        "> Tests are the source of truth; this file is a derived view.",
        "",
        "---",
        "",
    ]

    if not invariants:
        lines.extend([
            "_No invariants were detected._",
            "",
        ])
        return "\n".join(lines)

    for invariant in invariants:
        lines.extend([
            f"## `{invariant.name}`",
            "",
            f"**Source test:** `{invariant.source_file}`",
            "",
            invariant.description,
            "",
            "---",
            "",
        ])

    return "\n".join(lines)


# ---------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------

def main() -> None:
    invariants = extract_invariants()
    markdown = render_markdown(invariants)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(markdown, encoding="utf-8")

    print(f"[docgen] Generated {OUTPUT_FILE} ({len(invariants)} invariants)")


if __name__ == "__main__":
    main()