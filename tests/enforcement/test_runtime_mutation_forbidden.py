# tests/enforcement/test_runtime_mutation_forbidden.py

"""
ADR-OP-001
"""

from pathlib import Path
from .helpers import run_checker_on

def test_post_init_mutation_is_forbidden():
    result = run_checker_on(
        Path("tests/enforcement/fixtures/forbidden_post_init.py")
    )
    assert result.returncode != 0
    assert "outside constructor" in result.stdout.lower()

def test_lazy_init_is_forbidden():
    result = run_checker_on(
        Path("tests/enforcement/fixtures/forbidden_lazy_init.py")
    )
    assert result.returncode != 0
    assert "outside constructor" in result.stdout.lower()