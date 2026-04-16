from pathlib import Path

# ---------------------------------------------------------------------
# Jurisdiction Configuration
# ---------------------------------------------------------------------
#
# This module defines *governance jurisdiction*, not policy.
# It answers ONE question only:
#
#     "Is this file subject to AfriTech constitutional enforcement?"
#
# Tools, runners, and rules MUST respect this boundary and MUST NOT
# re-scan or override it.
#

IGNORED_ROOTS = {
    "_quarantine",      # explicit legacy / isolation
    "architecture",     # docs and diagrams
    "docs",             # documentation
    "tools",            # governance tools themselves
    "contracts",        # historical / deprecated APIs
    "venv",
    ".venv",
    "__pycache__",
    ".git",             # VCS metadata
    ".mypy_cache",
    ".pytest_cache",
    # "tests",          # intentionally NOT included by default
}

REPO_ROOT = Path(".").resolve()

# ---------------------------------------------------------------------
# Core Jurisdiction Logic
# ---------------------------------------------------------------------

def is_ignored(path: Path) -> bool:
    """
    Returns True if the given path MUST be excluded from governance.

    Exclusion rules (deny-first):
    1. Path cannot be resolved relative to REPO_ROOT
    2. Any directory component is in IGNORED_ROOTS
    3. Any parent directory (including repo root) contains a `.LEGACY` marker

    Notes:
    - Deny-by-default is intentional.
    - `.LEGACY` is a filesystem-level declaration of historical code.
    - Scope must be stable across refactors, CI, and developer machines.
    """
    try:
        rel = path.resolve().relative_to(REPO_ROOT)
    except Exception:
        # Outside repo root or invalid path → not governable
        return True

    parts = rel.parts
    if not parts:
        return True

    # -----------------------------------------------------------------
    # Rule 1: Ignore any path containing an ignored root component
    # -----------------------------------------------------------------
    if any(part in IGNORED_ROOTS for part in parts):
        return True

    # -----------------------------------------------------------------
    # Rule 2: `.LEGACY` marker anywhere up to repo root
    # -----------------------------------------------------------------
    current = REPO_ROOT / rel

    while True:
        if (current / ".LEGACY").exists():
            return True
        if current == REPO_ROOT:
            break
        current = current.parent

    return False


# ---------------------------------------------------------------------
# File Discovery (Governed Surface)
# ---------------------------------------------------------------------

def collect_files() -> list[str]:
    """
    Collect all Python files under governance jurisdiction.

    Returns:
        A list of repo-relative file paths (strings).

    Contract:
    - This is the ONLY approved file discovery mechanism.
    - Tools MUST NOT perform their own globbing.
    - All enforcement is constrained to this result.
    """
    files: list[str] = []

    for path in REPO_ROOT.rglob("*.py"):
        if is_ignored(path):
            continue

        try:
            rel_path = path.relative_to(REPO_ROOT)
            files.append(str(rel_path))
        except Exception:
            # Any resolution failure → ignore defensively
            continue

    return files