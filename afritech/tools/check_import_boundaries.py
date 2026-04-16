#!/usr/bin/env python3
from __future__ import annotations

"""
AfriTech Import Boundary Validator
=================================

Enforces architectural import boundaries between layers.

This tool is FAIL-CLOSED.
Any boundary violation causes CI failure.

Enforces: ADR-BI-003
"""

import ast
from pathlib import Path
from typing import Iterable

# ---------------------------------------------------------------------
# Layer definitions (AUTHORITATIVE)
# ---------------------------------------------------------------------

LAYERS = {
    "core": "afritech.platform.core",
    "control_plane": "afritech.platform.control_plane",
    "infrastructure": "afritech.platform.infrastructure",
}

# Who may import whom (directional)
ALLOWED_IMPORTS = {
    "core": set(),  # core imports nothing internal
    "control_plane": {"core"},
    "infrastructure": set(),  # infra is leaf-only
}

SKIP_DIRS = {
    "venv",
    ".venv",
    ".tox",
    "__pycache__",
    "site-packages",
}

# ---------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------

def should_skip(path: Path) -> bool:
    return any(part in SKIP_DIRS for part in path.parts)


def detect_layer(path: Path) -> str | None:
    for layer, root in LAYERS.items():
        if root.replace(".", "/") in path.as_posix():
            return layer
    return None


def iter_imports(path: Path) -> Iterable[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for n in node.names:
                yield n.name
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                yield node.module


# ---------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------

def validate_file(path: Path) -> list[str]:
    violations: list[str] = []

    layer = detect_layer(path)
    if layer is None:
        return violations

    for imported in iter_imports(path):
        for target_layer, root in LAYERS.items():
            if imported.startswith(root):
                if target_layer != layer and target_layer not in ALLOWED_IMPORTS[layer]:
                    violations.append(
                        f"{path}:{layer} → {target_layer} import forbidden ({imported})"
                    )

    return violations


# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------

def main() -> None:
    violations: list[str] = []

    for py in Path(".").rglob("*.py"):
        if should_skip(py):
            continue
        violations.extend(validate_file(py))

    if violations:
        print("❌ Import boundary violations detected:\n")
        for v in sorted(violations):
            print(f"  {v}")
        print(f"\nTotal violations: {len(violations)}")
        raise SystemExit(1)

    print("✅ Import boundary enforcement passed.")


if __name__ == "__main__":
    main()