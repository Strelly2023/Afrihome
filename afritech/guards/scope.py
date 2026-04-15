from pathlib import Path

IGNORED_ROOTS = {
    "_quarantine",
    "architecture",
    "docs",
    "tools",
    "contracts",
    "venv",
    ".venv",
    "__pycache__",
}

def is_ignored(path: Path) -> bool:
    """
    Returns True if the path MUST be excluded from governance.

    Exclusion rules:
    1. Root directory is ignored
    2. Any parent directory contains a .LEGACY marker
    """

    # Normalize
    try:
        parts = path.parts
    except Exception:
        return True

    # Rule 1: ignored roots
    if parts and parts[0] in IGNORED_ROOTS:
        return True

    # Rule 2: LEGACY markers
    for parent in path.parents:
        if (parent / ".LEGACY").exists():
            return True

    return False