from __future__ import annotations

"""
GA Core â€” Forbidden API Enforcement Tests
=========================================

These tests enforce the absolute safety constraints of
afritech.platform.core at GA.

They assert that the core:
- does NOT access real clocks or wall time
- does NOT use randomness or entropy
- does NOT perform IO or system interaction
- does NOT invoke frameworks, runtimes, or concurrency primitives

FAILURE OF ANY TEST IN THIS FILE MEANS:
â†’ CORE DETERMINISM OR PURITY HAS BEEN COMPROMISED
"""

from pathlib import Path
from typing import Dict, List

import pytest

from tools.core_enforcement.rules import (
    CORE_ROOT,
    FORBIDDEN_IMPORT_ROOTS,
    FORBIDDEN_PATTERNS,
)
from tools.core_enforcement.scanner import (
    extract_import_roots,
    scan_source_for_patterns,
    iter_python_files,
)


CORE_PATH = Path(CORE_ROOT)


# ============================================================
# Safety Sanity Checks
# ============================================================

def test_core_path_exists():
    """
    Core root directory must exist.
    """
    assert CORE_PATH.exists(), f"Core path does not exist: {CORE_PATH}"


def test_core_contains_python_files():
    """
    Core must contain at least one Python source file.
    """
    files = list(iter_python_files(CORE_PATH))
    assert files, (
        "No Python files found under core root â€” "
        "CORE_ROOT may be misconfigured or empty."
    )


# ============================================================
# Forbidden Import Root Enforcement
# ============================================================

def test_core_has_no_forbidden_import_roots():
    """
    Core MUST NOT import forbidden stdlib, framework, IO,
    concurrency, or persistence modules.

    Import root detection is ASTâ€‘based.
    """
    violations: Dict[str, List[str]] = {}

    for py_file in iter_python_files(CORE_PATH):
        import_roots = extract_import_roots(py_file)

        illegal = sorted(import_roots & FORBIDDEN_IMPORT_ROOTS)
        if illegal:
            violations[str(py_file)] = illegal

    if violations:
        details = "\n".join(
            f"- {file} â†’ {mods}" for file, mods in violations.items()
        )
        pytest.fail(
            "âŒ Forbidden import roots detected in core:\n\n"
            + details
        )


# ============================================================
# Forbidden Runtime Pattern Enforcement
# ============================================================

def test_core_has_no_forbidden_runtime_patterns():
    """
    Core MUST NOT invoke forbidden runtime APIs such as:
    - wall clocks (time.time, datetime.now, etc.)
    - randomness (random.*, uuid.uuid4)
    - IO / debugging (print, logging)
    """
    violations: Dict[str, List[str]] = {}

    for py_file in iter_python_files(CORE_PATH):
        found = sorted(scan_source_for_patterns(py_file, FORBIDDEN_PATTERNS))
        if found:
            violations[str(py_file)] = found

    if violations:
        details = "\n".join(
            f"- {file} â†’ {patterns}" for file, patterns in violations.items()
        )
        pytest.fail(
            "âŒ Forbidden runtime patterns detected in core:\n\n"
            + details
        )


# ============================================================
# Strict Mode â€” Lowâ€‘Level IO Guard
# ============================================================

@pytest.mark.parametrize(
    "pattern",
    [
        "print(",
        "logging.",
        "open(",
    ],
)
def test_no_basic_io_primitives(pattern: str):
    """
    Extra defensive check against basic IO primitives that
    may bypass higherâ€‘level pattern filters.

    This is intentionally a raw text scan.
    """
    offenders: List[str] = []

    for py_file in iter_python_files(CORE_PATH):
        try:
            content = py_file.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            pytest.fail(f"Could not decode source file: {py_file}")

        if pattern in content:
            offenders.append(str(py_file))

    assert not offenders, (
        f"âŒ Forbidden IO primitive '{pattern}' detected in:\n"
        + "\n".join(offenders)
    )
