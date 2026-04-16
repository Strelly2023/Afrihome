from __future__ import annotations
"""
AST-based scanners for AfriTech Core enforcement (GA).

This module contains NO business logic.
It provides deterministic, static analysis helpers only.

RULES:
- Test / enforcement support ONLY
- No runtime use
- No imports from afritech.platform.core
- Pure, deterministic behavior
"""

import ast
from pathlib import Path
from typing import Set, Iterable


# ---------------------------------------------------------------------
# Core AST utilities
# ---------------------------------------------------------------------

def parse_python_file(py_file: Path) -> ast.Module:
    """
    Parse a Python file into an AST.

    Raises:
        SyntaxError if the file is invalid Python.
    """
    return ast.parse(py_file.read_text(encoding="utf-8"))


# ---------------------------------------------------------------------
# Import scanning
# ---------------------------------------------------------------------

def extract_import_roots(py_file: Path) -> Set[str]:
    """
    Extract top-level import roots from a Python file.

    Examples:
        import a.b.c        -> {"a"}
        import a            -> {"a"}
        from a.b import c   -> {"a"}
        from a import b     -> {"a"}

    Returns:
        Set[str]: root module names
    """
    tree = parse_python_file(py_file)
    roots: Set[str] = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for name in node.names:
                root = name.name.split(".", 1)[0]
                roots.add(root)

        elif isinstance(node, ast.ImportFrom):
            # node.module may be None for relative imports: "from . import x"
            if node.module:
                root = node.module.split(".", 1)[0]
                roots.add(root)

    return roots


def extract_full_imports(py_file: Path) -> Set[str]:
    """
    Extract full import paths (not just roots).

    Examples:
        import a.b.c        -> {"a.b.c"}
        from a.b import c   -> {"a.b"}
    """
    tree = parse_python_file(py_file)
    imports: Set[str] = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for name in node.names:
                imports.add(name.name)

        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.add(node.module)

    return imports


# ---------------------------------------------------------------------
# String pattern scanning (last-resort guardrails)
# ---------------------------------------------------------------------

def scan_source_for_patterns(
    py_file: Path,
    patterns: Iterable[str],
) -> Set[str]:
    """
    Scan raw source for forbidden string patterns.

    This is intentionally NOT AST-based and is used only
    as a safety net against nondeterministic or forbidden calls
    (e.g., time.time, random, uuid).

    Returns:
        Set[str]: patterns found in source
    """
    source = py_file.read_text(encoding="utf-8")
    found: Set[str] = set()

    for pattern in patterns:
        if pattern in source:
            found.add(pattern)

    return found


# ---------------------------------------------------------------------
# Generic file utilities
# ---------------------------------------------------------------------

def iter_python_files(root: Path) -> Iterable[Path]:
    """
    Yield all *.py files under a directory, deterministically.

    Sorting ensures stable traversal order across platforms.
    """
    yield from sorted(root.rglob("*.py"))
