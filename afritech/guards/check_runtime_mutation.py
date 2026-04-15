#!/usr/bin/env python3
from __future__ import annotations

"""
AfriTech Runtime Mutation Validator
==================================

Enforces ADR-OP-001 — Runtime Mutation Outside Constructors Prohibition.

Mutation model enforced:
- No instance mutation outside __init__
- No instance attribute deletion
- No class attribute mutation at runtime
- No container mutation on instance/class attributes
- No __setattr__ overrides
- No __delattr__ overrides
- No descriptor setters (@property.setter / __set__)
- No metaclass __setattr__

FAIL-CLOSED:
Any violation blocks CI / pre-commit.
"""

import ast
from pathlib import Path

# ---------------------------------------------------------------------
# Enforcement scope
# ---------------------------------------------------------------------

ENFORCED_ROOTS = {
    "afritech/platform/core",
    "afritech/platform/control_plane",
}

SKIP_DIRS = {
    "venv", ".venv", ".tox", "__pycache__", "site-packages",
    "tests", "tools", "config", "_quarantine", "core_PRE_GA_BACKUP",
}

# ---------------------------------------------------------------------
# Scope helpers
# ---------------------------------------------------------------------

def should_skip(path: Path) -> bool:
    if any(p in SKIP_DIRS for p in path.parts):
        return True
    return any(root in path.as_posix() for root in ENFORCED_ROOTS)

# ---------------------------------------------------------------------
# AST helpers
# ---------------------------------------------------------------------

def is_property_setter(fn: ast.FunctionDef) -> bool:
    return any(
        isinstance(d, ast.Attribute) and d.attr == "setter"
        for d in fn.decorator_list
    )

def is_descriptor_with_set(cls: ast.ClassDef) -> bool:
    return any(
        isinstance(n, ast.FunctionDef) and n.name == "__set__"
        for n in cls.body
    )

def is_metaclass(cls: ast.ClassDef) -> bool:
    return any(
        isinstance(b, ast.Name) and b.id == "type"
        for b in cls.bases
    )

# ---------------------------------------------------------------------
# Visitor
# ---------------------------------------------------------------------

class MutationVisitor(ast.NodeVisitor):
    def __init__(self, path: Path):
        self.path = path
        self.violations: list[str] = []
        self.current_class: str | None = None
        self.current_function: str | None = None
        self.known_classes: set[str] = set()

    # ---------------------------------------------------------
    # Class rules
    # ---------------------------------------------------------

    def visit_ClassDef(self, node: ast.ClassDef):
        self.known_classes.add(node.name)

        # ❌ Descriptor mutation via __set__
        if is_descriptor_with_set(node):
            self.violations.append(
                f"{self.path}:{node.lineno} — forbidden descriptor __set__ in class '{node.name}'"
            )

        # ❌ Metaclass __setattr__
        if is_metaclass(node):
            for fn in node.body:
                if isinstance(fn, ast.FunctionDef) and fn.name == "__setattr__":
                    self.violations.append(
                        f"{self.path}:{fn.lineno} — forbidden metaclass __setattr__ in metaclass '{node.name}'"
                    )

        prev = self.current_class
        self.current_class = node.name
        self.generic_visit(node)
        self.current_class = prev

    # ---------------------------------------------------------
    # Function rules
    # ---------------------------------------------------------

    def visit_FunctionDef(self, node: ast.FunctionDef):
        prev = self.current_function
        self.current_function = node.name

        # ❌ __setattr__ override
        if node.name == "__setattr__" and self.current_class:
            self.violations.append(
                f"{self.path}:{node.lineno} — forbidden __setattr__ in class '{self.current_class}'"
            )

        # ❌ __delattr__ override
        if node.name == "__delattr__" and self.current_class:
            self.violations.append(
                f"{self.path}:{node.lineno} — forbidden __delattr__ in class '{self.current_class}'"
            )

        # ❌ @property.setter
        if self.current_class and is_property_setter(node):
            self.violations.append(
                f"{self.path}:{node.lineno} — forbidden @property.setter in class '{self.current_class}'"
            )

        self.generic_visit(node)
        self.current_function = prev

    # ---------------------------------------------------------
    # Assignment rules
    # ---------------------------------------------------------

    def visit_Assign(self, node: ast.Assign):
        for t in node.targets:

            # Instance mutation
            if (
                self.current_class
                and self.current_function != "__init__"
                and isinstance(t, ast.Attribute)
                and isinstance(t.value, ast.Name)
                and t.value.id == "self"
            ):
                self.violations.append(
                    f"{self.path}:{node.lineno} — instance mutation self.{t.attr} outside __init__"
                )

            # Class attribute mutation
            if (
                isinstance(t, ast.Attribute)
                and isinstance(t.value, ast.Name)
                and t.value.id in self.known_classes
            ):
                self.violations.append(
                    f"{self.path}:{node.lineno} — class mutation {t.value.id}.{t.attr}"
                )

            # cls.attr mutation
            if (
                isinstance(t, ast.Attribute)
                and isinstance(t.value, ast.Name)
                and t.value.id == "cls"
            ):
                self.violations.append(
                    f"{self.path}:{node.lineno} — class mutation via cls.{t.attr}"
                )

            # type(self).attr mutation
            if (
                isinstance(t, ast.Attribute)
                and isinstance(t.value, ast.Call)
                and isinstance(t.value.func, ast.Name)
                and t.value.func.id == "type"
            ):
                self.violations.append(
                    f"{self.path}:{node.lineno} — class mutation via type(self)"
                )

            # Container mutation on instance/class attr
            if isinstance(t, ast.Subscript):
                base = t.value
                if isinstance(base, ast.Attribute):
                    if (
                        isinstance(base.value, ast.Name)
                        and base.value.id in {"self", "cls"}
                    ):
                        self.violations.append(
                            f"{self.path}:{node.lineno} — container mutation on {base.value.id}.{base.attr}"
                        )

        self.generic_visit(node)

    # ---------------------------------------------------------
    # Delete rules
    # ---------------------------------------------------------

    def visit_Delete(self, node: ast.Delete):
        for t in node.targets:

            # Instance attribute deletion
            if (
                self.current_class
                and isinstance(t, ast.Attribute)
                and isinstance(t.value, ast.Name)
                and t.value.id == "self"
            ):
                self.violations.append(
                    f"{self.path}:{node.lineno} — deletion of self.{t.attr}"
                )

            # Class attribute deletion
            if (
                isinstance(t, ast.Attribute)
                and isinstance(t.value, ast.Name)
                and t.value.id in self.known_classes
            ):
                self.violations.append(
                    f"{self.path}:{node.lineno} — deletion of class attribute {t.value.id}.{t.attr}"
                )

        self.generic_visit(node)

# ---------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------

def find_violations(path: Path) -> list[str]:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except SyntaxError:
        return []

    visitor = MutationVisitor(path)
    visitor.visit(tree)
    return visitor.violations

# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------

def main() -> None:
    violations: list[str] = []

    for py in Path(".").rglob("*.py"):
        if should_skip(py):
            continue
        violations.extend(find_violations(py))

    if violations:
        print("❌ Runtime mutation violations detected:\n")
        for v in sorted(violations):
            print(f"  {v}")
        raise SystemExit(1)

    print("✅ Runtime mutation outside constructors check passed.")

if __name__ == "__main__":
    main()