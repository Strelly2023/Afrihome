from __future__ import annotations
#tools/core_enforcement/enforce_core.py
"""
AfriTech Core Enforcement Script (GA)

This script enforces the architectural constitution defined in:
    tools/core_enforcement/rules.py

It MUST be run in CI and locally.
Any violation is a GA-sealed architecture failure.
"""

# ---------------------------------------------------------------------
# Bootstrap (allows direct execution without -m)
# ---------------------------------------------------------------------

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# ---------------------------------------------------------------------
# Standard library imports
# ---------------------------------------------------------------------

import ast
from typing import Set, Iterable, List

# ---------------------------------------------------------------------
# Rule imports (single source of constitutional truth)
# ---------------------------------------------------------------------

from tools.core_enforcement.rules import (
    CORE_ROOT,
    CORE_IMPORT_RULES,
    KERNEL_FORBIDDEN_IMPORT_ROOTS,
    FORBIDDEN_IMPORT_ROOTS,
    FORBIDDEN_PATTERNS,
    MODULE_FORBIDDEN_VOCAB,
    TYPING_ALLOWED_EXCEPTION_NAMES,
)

# ---------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------

CORE_ROOT_PATH = Path(CORE_ROOT).resolve()

# ---------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------

def iter_python_files(root: Path) -> Iterable[Path]:
    for path in root.rglob("*.py"):
        if "__pycache__" not in path.parts:
            yield path


def module_name_from_path(path: Path) -> str:
    """
    Convert a file path to its core module name.

    Example:
        afritech/platform/core/policy/evaluation.py -> "policy"
    """
    parts = path.parts
    try:
        core_idx = parts.index("core")
        return parts[core_idx + 1]
    except (ValueError, IndexError):
        return "<unknown>"


def parse_imports(tree: ast.AST) -> Set[str]:
    imports: Set[str] = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.add(node.module)

    return imports

# ---------------------------------------------------------------------
# Enforcement Rules
# ---------------------------------------------------------------------

def enforce_kernel_isolation(module: str, imports: Set[str], path: Path):
    if module != "kernel":
        return

    for imp in imports:
        for forbidden in KERNEL_FORBIDDEN_IMPORT_ROOTS:
            if imp.startswith(forbidden):
                raise RuntimeError(
                    f"[KERNEL VIOLATION] {path} imports '{imp}' â€” "
                    f"kernel must not import anything from core"
                )


def enforce_forbidden_import_roots(imports: Set[str], path: Path):
    for imp in imports:
        root = imp.split(".")[0]
        if root in FORBIDDEN_IMPORT_ROOTS:
            raise RuntimeError(
                f"[FORBIDDEN IMPORT] {path} imports '{imp}' "
                f"(root '{root}' is forbidden in core)"
            )


def enforce_core_import_rules(module: str, imports: Set[str], path: Path):
    if module not in CORE_IMPORT_RULES:
        raise RuntimeError(
            f"[UNKNOWN MODULE] {path} belongs to unknown core module '{module}'"
        )

    allowed = CORE_IMPORT_RULES[module]

    for imp in imports:
        if not imp.startswith("afritech.platform.core"):
            continue

        parts = imp.split(".")
        try:
            core_idx = parts.index("core")
            imported_module = parts[core_idx + 1]
        except (ValueError, IndexError):
            continue

        if imported_module == module:
            continue  # self-import allowed

        if imported_module not in allowed:
            raise RuntimeError(
                f"[IMPORT VIOLATION] {path} ({module}) imports core.{imported_module} "
                f"but may only import {allowed}"
            )


def enforce_forbidden_patterns(source: str, path: Path):
    for pattern in FORBIDDEN_PATTERNS:
        if pattern in source:
            raise RuntimeError(
                f"[FORBIDDEN PATTERN] {path} contains '{pattern}'"
            )


def enforce_vocab_purity(module: str, tree: ast.AST, path: Path):
    """
    Enforce vocabulary purity using AST identifiers ONLY.
    Docstrings and comments are ignored.
    """
    forbidden = MODULE_FORBIDDEN_VOCAB.get(module)
    if not forbidden:
        return

    forbidden = {word.lower() for word in forbidden}

    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            if node.id.lower() in forbidden:
                raise RuntimeError(
                    f"[VOCAB VIOLATION] {path} uses forbidden identifier "
                    f"'{node.id}' for module '{module}'"
                )
        elif isinstance(node, ast.Attribute):
            if node.attr.lower() in forbidden:
                raise RuntimeError(
                    f"[VOCAB VIOLATION] {path} accesses forbidden attribute "
                    f"'{node.attr}' for module '{module}'"
                )


def enforce_typing_exceptions(tree: ast.AST, path: Path):
    """
    typing may only raise ValidationError
    """
    for node in ast.walk(tree):
        if isinstance(node, ast.Raise):
            if node.exc and isinstance(node.exc, ast.Name):
                if node.exc.id not in TYPING_ALLOWED_EXCEPTION_NAMES:
                    raise RuntimeError(
                        f"[TYPING VIOLATION] {path} raises '{node.exc.id}' "
                        f"but typing may only raise {TYPING_ALLOWED_EXCEPTION_NAMES}"
                    )

# ---------------------------------------------------------------------
# Main Entry Point
# ---------------------------------------------------------------------

def run_enforcement():
    failures: List[str] = []

    for path in iter_python_files(CORE_ROOT_PATH):

        # Skip top-level core/__init__.py
        if path.name == "__init__.py" and path.parent == CORE_ROOT_PATH:
            continue

        module = module_name_from_path(path)
        source = path.read_text(encoding="utf-8")

        try:
            tree = ast.parse(source)
            imports = parse_imports(tree)

            enforce_kernel_isolation(module, imports, path)
            enforce_forbidden_import_roots(imports, path)
            enforce_core_import_rules(module, imports, path)
            enforce_forbidden_patterns(source, path)
            enforce_vocab_purity(module, tree, path)

            if module == "typing":
                enforce_typing_exceptions(tree, path)

        except RuntimeError as e:
            failures.append(str(e))

    if failures:
        raise SystemExit(
            "\n\nðŸš« CORE ARCHITECTURE VIOLATIONS DETECTED:\n\n"
            + "\n".join(failures)
        )

    print("âœ… Core architecture enforcement passed (GAâ€‘sealed)")


if __name__ == "__main__":
    run_enforcement()
