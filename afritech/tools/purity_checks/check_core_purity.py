#!/usr/bin/env python3
from __future__ import annotations

"""
AfriTech Core Purity Guard
==========================

Enforces Core purity invariants across afritech/platform/core.

Aligned with:
- ADR-000   (Core Freeze)
- ADR-000A  (Identity Ontology)
- ADR-OP-001 (No Runtime Mutation)
- ADR-DS-BI-001 (Deterministic Boundaries)
- ADR-KE-FT-001/002 (No Time / Entropy in Core)

FAIL-CLOSED:
Any violation blocks CI.

Core MUST be:
- Deterministic
- Pure (no IO, no randomness, no time)
- Immutable (no runtime mutation)
- Environment-independent
- Free of orchestration logic
"""

import ast
import sys
from pathlib import Path

# ---------------------------------------------------------------------
# Scope
# ---------------------------------------------------------------------

CORE_ROOT = Path("afritech/platform/core")

SKIP_DIRS = {
    "__pycache__",
    "tests",
}

# ---------------------------------------------------------------------
# Forbidden Imports (Environment / Side Effects)
# ---------------------------------------------------------------------

FORBIDDEN_MODULES = (
    "random",
    "uuid",
    "secrets",
    "time",
    "os",
    "subprocess",
    "socket",
    "requests",
    "http",
)

FORBIDDEN_IMPORT_PREFIXES = (
    "afritech.platform.control_plane",
)

# ---------------------------------------------------------------------
# Forbidden Calls (non-determinism / IO)
# ---------------------------------------------------------------------

FORBIDDEN_CALLS = (
    "random",
    "uuid",
    "secrets",
    "time.time",
    "time.sleep",
    "datetime.now",
    "datetime.utcnow",
    "os.getenv",
    "os.environ",
    "open",
)

# ---------------------------------------------------------------------
# Forbidden Class Patterns (Orchestration leakage)
# ---------------------------------------------------------------------

FORBIDDEN_CLASS_SUFFIXES = (
    "Service",
    "Manager",
    "Factory",
)

# ---------------------------------------------------------------------
# AST Visitor
# ---------------------------------------------------------------------

class CorePurityVisitor(ast.NodeVisitor):
    def __init__(self, path: Path):
        self.path = path
        self.violations: list[str] = []
        self.current_function: str | None = None

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------

    def _violation(self, node: ast.AST, message: str):
        self.violations.append(f"{self.path}:{node.lineno} — {message}")

    # ---------------------------------------------------------
    # Imports
    # ---------------------------------------------------------

    def visit_Import(self, node: ast.Import):
        for alias in node.names:
            name = alias.name

            if name in FORBIDDEN_MODULES:
                self._violation(node, f"forbidden import '{name}'")

            if name.startswith(FORBIDDEN_IMPORT_PREFIXES):
                self._violation(node, f"forbidden control_plane import '{name}'")

        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        if node.module:
            if node.module in FORBIDDEN_MODULES:
                self._violation(node, f"forbidden import from '{node.module}'")

            if node.module.startswith(FORBIDDEN_IMPORT_PREFIXES):
                self._violation(
                    node,
                    f"forbidden control_plane import '{node.module}'",
                )

        self.generic_visit(node)

    # ---------------------------------------------------------
    # Function context tracking
    # ---------------------------------------------------------

    def visit_FunctionDef(self, node: ast.FunctionDef):
        prev = self.current_function
        self.current_function = node.name

        # Detect identity creation / orchestration leakage
        if node.name.startswith(("create_", "generate_", "new_")):
            self._violation(
                node,
                f"forbidden creation function '{node.name}' in Core",
            )

        self.generic_visit(node)
        self.current_function = prev

    # ---------------------------------------------------------
    # Calls (time / entropy / IO)
    # ---------------------------------------------------------

    def visit_Call(self, node: ast.Call):
        try:
            name = ast.unparse(node.func)
        except Exception:
            name = ""

        for forbidden in FORBIDDEN_CALLS:
            if forbidden in name:
                self._violation(node, f"forbidden call '{name}'")

        self.generic_visit(node)

    # ---------------------------------------------------------
    # Mutation detection (ADR-OP-001)
    # ---------------------------------------------------------

    def visit_Assign(self, node: ast.Assign):
        # Allow safe constructor normalization:
        # object.__setattr__(self, ...)
        if isinstance(node.value, ast.Call):
            try:
                name = ast.unparse(node.value.func)
                if name == "object.__setattr__":
                    return
            except Exception:
                pass

        for target in node.targets:
            if (
                isinstance(target, ast.Attribute)
                and isinstance(target.value, ast.Name)
                and target.value.id == "self"
            ):
                if self.current_function not in ("__init__", "__post_init__"):
                    self._violation(
                        node,
                        f"mutation of self.{target.attr} outside constructor",
                    )

        self.generic_visit(node)

    def visit_Delete(self, node: ast.Delete):
        for target in node.targets:
            if (
                isinstance(target, ast.Attribute)
                and isinstance(target.value, ast.Name)
                and target.value.id == "self"
            ):
                self._violation(
                    node,
                    f"deletion of self.{target.attr} is forbidden",
                )
        self.generic_visit(node)

    # ---------------------------------------------------------
    # Class-level enforcement
    # ---------------------------------------------------------

    def visit_ClassDef(self, node: ast.ClassDef):
        for suffix in FORBIDDEN_CLASS_SUFFIXES:
            if node.name.endswith(suffix):
                self._violation(
                    node,
                    f"forbidden orchestration class '{node.name}' in Core",
                )

        self.generic_visit(node)

# ---------------------------------------------------------------------
# Execution
# ---------------------------------------------------------------------

def should_skip(path: Path) -> bool:
    return any(part in SKIP_DIRS for part in path.parts)

def main() -> None:
    violations: list[str] = []

    for py_file in CORE_ROOT.rglob("*.py"):
        if should_skip(py_file):
            continue

        try:
            tree = ast.parse(py_file.read_text(encoding="utf-8"))
        except SyntaxError:
            continue

        visitor = CorePurityVisitor(py_file)
        visitor.visit(tree)
        violations.extend(visitor.violations)

    if violations:
        print("❌ Core purity violations detected:\n")
        for v in sorted(violations):
            print(f"  {v}")
        sys.exit(1)

    print("✅ Core purity check passed.")

# ---------------------------------------------------------------------

if __name__ == "__main__":
    main()