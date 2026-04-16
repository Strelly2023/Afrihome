#!/usr/bin/env python3
from __future__ import annotations

"""
AfriTech CI — Identity Creation Guard
====================================

Enforces Core Identity Purity (ADR-IDENTITY-001)

Core identity MUST NOT:
- generate entropy
- import entropy providers
- orchestrate identity creation
- define identity services

Core identity MAY:
- define identity semantics
- validate identity values
- normalize identity inputs

FAIL-CLOSED:
Any violation blocks CI.
"""

import ast
import sys
from pathlib import Path

# ---------------------------------------------------------------------
# Scope
# ---------------------------------------------------------------------

CORE_IDENTITY_ROOT = Path("afritech/platform/core/identity")

# ---------------------------------------------------------------------
# Forbidden imports
# ---------------------------------------------------------------------

FORBIDDEN_IMPORT_PREFIXES = (
    "afritech.platform.control_plane.entropy",
)

FORBIDDEN_MODULES = (
    "uuid",
    "random",
    "secrets",
)

# ---------------------------------------------------------------------
# Forbidden naming patterns (creation semantics)
# ---------------------------------------------------------------------

FORBIDDEN_NAME_PREFIXES = (
    "create_",
    "generate_",
    "new_",
)

# ---------------------------------------------------------------------
# AST Visitor
# ---------------------------------------------------------------------

class IdentityCreationVisitor(ast.NodeVisitor):
    def __init__(self, path: Path):
        self.path = path
        self.violations: list[str] = []

    # -----------------------------
    # Imports
    # -----------------------------

    def visit_Import(self, node: ast.Import):
        for alias in node.names:
            name = alias.name

            if name in FORBIDDEN_MODULES or name.startswith(FORBIDDEN_IMPORT_PREFIXES):
                self._violation(
                    node,
                    f"forbidden import '{name}' in Core identity",
                )

        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        if node.module:
            module = node.module

            if module in FORBIDDEN_MODULES or module.startswith(FORBIDDEN_IMPORT_PREFIXES):
                self._violation(
                    node,
                    f"forbidden import from '{module}' in Core identity",
                )

        self.generic_visit(node)

    # -----------------------------
    # Function definitions
    # -----------------------------

    def visit_FunctionDef(self, node: ast.FunctionDef):
        if node.name.startswith(FORBIDDEN_NAME_PREFIXES):
            self._violation(
                node,
                f"identity creation function '{node.name}' defined in Core",
            )

        self.generic_visit(node)

    # -----------------------------
    # Helpers
    # -----------------------------

    def _violation(self, node: ast.AST, message: str):
        self.violations.append(
            f"{self.path}:{node.lineno} — {message}"
        )

# ---------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------

def find_violations() -> list[str]:
    violations: list[str] = []

    for py_file in CORE_IDENTITY_ROOT.rglob("*.py"):
        try:
            tree = ast.parse(py_file.read_text(encoding="utf-8"))
        except SyntaxError as exc:
            violations.append(f"{py_file}:{exc.lineno} — syntax error: {exc.msg}")
            continue

        visitor = IdentityCreationVisitor(py_file)
        visitor.visit(tree)
        violations.extend(visitor.violations)

    return sorted(violations)

# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------

def main() -> None:
    violations = find_violations()

    if violations:
        print("❌ Core identity creation violations detected:\n")
        for v in violations:
            print(f"  {v}")
        sys.exit(1)

    print("✅ Identity creation guard passed (Core identity is pure).")


if __name__ == "__main__":
    main()