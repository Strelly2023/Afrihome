# tests/enforcement/test_runtime_mutation_allowed.py

"""
ADR-OP-001
"""

from pathlib import Path
from .helpers import run_runtime_checker


def test_assignment_only_in_init_is_allowed():
    result = run_runtime_checker(
        Path("tests/enforcement/fixtures/allowed_init_only.py")
    )
    assert result.returncode == 0
    assert "passed" in result.stdout.lower()


def test_factory_replacement_is_allowed():
    result = run_runtime_checker(
        Path("tests/enforcement/fixtures/allowed_factory_replacement.py")
    )
    assert result.returncode == 0
    assert "passed" in result.stdout.lower()


def test_checker_passes_entire_repo_snapshot():
    """
    Sanity guard: prove that the rule holds when applied globally.
    This must ALWAYS pass on main.
    """
    result = run_runtime_checker(Path("."))
    assert result.returncode == 0