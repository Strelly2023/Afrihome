from __future__ import annotations
"""
GA Core Test Utilities
---------------------

Purpose:
- Provide deterministic helpers for architectural enforcement tests
- Keep isolation logic centralized and reusable
- Depend on stdlib only

THIS FILE IS TEST-ONLY.
It MUST NOT import any application or core modules.
"""

import ast
from pathlib import Path
from typing import Set


# ============================================================
# Import Extraction Utility
# ============================================================

def extract_full_imports(path: Path) -> Set[str]:
    """
    Extract all fully-qualified import paths from a Python file.

    This inspects:
    - `import x.y.z`
    - `from x.y import a, b`

    Returns:
        A set of strings such as:
        {
            "afritech.platform.core.identity",
            "afritech.platform.core.rbac.permission",
            ...
        }

    Notes:
    - Relative imports are ignored
    - Syntax errors are tolerated (file is skipped)
    - Stdlib imports are ignored later by callers
    """
    if not path.exists():
        return set()

    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
    except (SyntaxError, UnicodeDecodeError):
        # Tests must never crash on bad files
        return set()

    imports: Set[str] = set()

    for node in ast.walk(tree):
        # import a.b.c
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name:
                    imports.add(alias.name)

        # from a.b.c import x
        elif isinstance(node, ast.ImportFrom):
            # Ignore relative imports
            if node.module and not node.level:
                imports.add(node.module)

    return imports
