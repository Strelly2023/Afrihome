#!/usr/bin/env python3
from __future__ import annotations

"""
AfriTech Global Mutable State Validator
======================================

Enforces:
- ADR-BI-004 — Global Mutable State Prohibition
- ADR-BI-005 — Forbidden Singleton Pattern
- ADR-BI-006 — Lazy Global Cache Prohibition

This validator forbids:
- runtime-mutable global containers
- forbidden singleton instances
- lazy/deferred global caches

While explicitly allowing constitutionally valid globals such as:
- export surfaces (__all__)
- constants (UPPER_CASE)
- semantic identity / permission types
- typing aliases and variance helpers
- regex patterns
- enums and immutable type-level constructs

FAIL-CLOSED:
Any violation must block CI / pre-commit.
"""

import ast
from pathlib import Path
from typing import Iterable

# ---------------------------------------------------------------------
# Enforcement scope (constitutional authority)
# ---------------------------------------------------------------------

# Only these roots are governed by BI-004 / BI-005 / BI-006
ENFORCED_ROOTS = {
    "afritech/platform/core",
    "afritech/platform/control_plane",
}

# Explicitly excluded domains (out of scope)
SKIP_DIRS = {
    "venv",
    ".venv",
    ".tox",
    "__pycache__",
    "site-packages",
    "tests",
    "tools",
    "config",
    "_quarantine",
    "core_PRE_GA_BACKUP",
}

# ---------------------------------------------------------------------
# Constitutionally allowed globals
# ---------------------------------------------------------------------

ALLOWED_NAMES = {
    "__all__",
    "__version__",
    "__name__",
}

ALLOWED_TYPE_NAMES = {
    "Permission",
    "ID_co",
}

ALLOWED_TYPE_NAME_SUFFIXES = (
    "Id",
    "Name",
    "Key",
    "Version",
    "Millis",
)

ALLOWED_CALL_PREFIXES = (
    "re.compile",
    "typing.NewType",
    "typing.TypeVar",
    "typing.Final",
    "typing.Literal",
    "typing.Union",
    "typing.Optional",
    "enum.Enum",
)

# ---------------------------------------------------------------------
# Forbidden singleton signals (ADR-BI-005)
# ---------------------------------------------------------------------

FORBIDDEN_SINGLETON_NAME_HINTS = (
    "engine",
    "client",
    "registry",
    "manager",
    "service",
    "provider",
    "singleton",
)

# ---------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------

def should_skip(path: Path) -> bool:
    """Return True if path is outside constitutional enforcement scope."""
    if any(part in SKIP_DIRS for part in path.parts):
        return True
    return not any(root in path.as_posix() for root in ENFORCED_ROOTS)


def is_mutable_container(node: ast.AST) -> bool:
    return isinstance(node, (ast.List, ast.Dict, ast.Set))


def is_call(node: ast.AST) -> bool:
    return isinstance(node, ast.Call)


def call_name(node: ast.Call) -> str:
    try:
        if isinstance(node.func, ast.Attribute):
            return f"{ast.unparse(node.func.value)}.{node.func.attr}"
        return ast.unparse(node.func)
    except Exception:
        return ""


def is_allowed_call(node: ast.Call) -> bool:
    name = call_name(node)
    return any(name.startswith(p) for p in ALLOWED_CALL_PREFIXES)


def is_allowed_type_name(name: str) -> bool:
    return (
        name in ALLOWED_NAMES
        or name in ALLOWED_TYPE_NAMES
        or name.isupper()
        or name.endswith(ALLOWED_TYPE_NAME_SUFFIXES)
    )


def looks_like_singleton_name(name: str) -> bool:
    lname = name.lower()
    return lname.startswith("_") or any(
        lname == hint or lname.endswith(hint)
        for hint in FORBIDDEN_SINGLETON_NAME_HINTS
    )


def is_sentinel(node: ast.AST) -> bool:
    """Detect common lazy-cache sentinels."""
    return (
        isinstance(node, ast.Constant)
        and node.value in (None,)
    ) or isinstance(node, ast.Tuple) and len(node.elts) == 0

# ---------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------

def find_global_mutable_violations(path: Path) -> list[str]:
    """
    Scan a file for:
    - global mutable containers
    - forbidden singletons
    - lazy global caches
    """
    violations: list[str] = []

    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except SyntaxError:
        return violations

    # Track global sentinel assignments for lazy cache detection
    sentinel_globals: set[str] = set()
    reassigned_globals: set[str] = set()

    # First pass: record global assignments
    for node in tree.body:
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets: list[ast.Name] = []
            value = None

            if isinstance(node, ast.Assign):
                targets = [t for t in node.targets if isinstance(t, ast.Name)]
                value = node.value
            else:
                if isinstance(node.target, ast.Name):
                    targets = [node.target]
                    value = node.value

            if not targets or value is None:
                continue

            for target in targets:
                name = target.id

                if is_allowed_type_name(name):
                    continue

                if is_mutable_container(value):
                    violations.append(
                        f"{path}:{node.lineno} — mutable global '{name}' is forbidden"
                    )
                    continue

                if is_call(value) and not is_allowed_call(value):
                    if looks_like_singleton_name(name):
                        violations.append(
                            f"{path}:{node.lineno} — forbidden singleton '{name}' detected"
                        )
                    else:
                        violations.append(
                            f"{path}:{node.lineno} — global '{name}' may hide mutable runtime state"
                        )

                if is_sentinel(value):
                    sentinel_globals.add(name)

    # Second pass: detect reassignment / mutation of sentinel globals (lazy caches)
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id in sentinel_globals:
                    reassigned_globals.add(target.id)

    for name in reassigned_globals:
        violations.append(
            f"{path} — lazy global cache '{name}' detected (sentinel → mutation)"
        )

    return violations

# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------

def iter_python_files(root: Path) -> Iterable[Path]:
    yield from root.rglob("*.py")


def main() -> None:
    violations: list[str] = []

    for py in iter_python_files(Path(".")):
        if should_skip(py):
            continue
        violations.extend(find_global_mutable_violations(py))

    if violations:
        print("❌ Global mutable state / singleton / lazy cache violations detected:\n")
        for v in sorted(violations):
            print(f"  {v}")
        print(f"\nTotal violations: {len(violations)}")
        raise SystemExit(1)

    print("✅ Global mutable state / singleton / lazy cache check passed.")


if __name__ == "__main__":
    main()
