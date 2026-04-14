from __future__ import annotations

"""
GA Core â€” Module Purity Enforcement Tests
========================================

These tests enforce semantic purity guarantees for
afritech.platform.core at GA.

Purity rules apply ONLY to executable semantics.
Documentation, comments, and docstrings are explicitly excluded.

FAILURE OF ANY TEST IN THIS FILE MEANS:
â†’ CORE ARCHITECTURE HAS BEEN VIOLATED
"""

from pathlib import Path
import ast

from tools.core_enforcement.rules import (
    CORE_ROOT,
    MODULE_FORBIDDEN_VOCAB,
)


CORE_PATH = Path(CORE_ROOT)


# =============================================================
# Helpers
# =============================================================

def extract_executable_identifiers(source: str) -> set[str]:
    """
    Extract identifier names from executable code only.
    This deliberately ignores:
    - comments
    - docstrings
    - string literals used only for documentation
    """
    tree = ast.parse(source)

    identifiers: set[str] = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            identifiers.add(node.id.lower())
        elif isinstance(node, ast.Attribute):
            identifiers.add(node.attr.lower())

    return identifiers


def assert_module_purity(module_name: str) -> None:
    """
    Assert that a core module does NOT use forbidden semantics
    in executable code.

    Forbidden vocabulary is defined in rules.py.
    """
    module_path = CORE_PATH / module_name

    if not module_path.exists():
        return

    forbidden_terms = MODULE_FORBIDDEN_VOCAB.get(module_name)
    if not forbidden_terms:
        return

    for py_file in module_path.rglob("*.py"):
        source = py_file.read_text(encoding="utf-8")

        identifiers = extract_executable_identifiers(source)

        for term in forbidden_terms:
            assert term not in identifiers, (
                "âŒ Core module purity violation detected\n\n"
                f"Module: {module_name}\n"
                f"File: {py_file}\n"
                f"Forbidden semantic identifier used: '{term}'\n"
                "This indicates executable responsibility drift.\n"
            )


# =============================================================
# Moduleâ€‘specific purity tests
# =============================================================

def test_tenancy_is_grammar_only():
    """
    tenancy MUST be grammarâ€‘only.
    """
    assert_module_purity("tenancy")


def test_identity_is_model_only():
    """
    identity MUST define models only.
    """
    assert_module_purity("identity")


def test_policy_is_condition_logic_only():
    """
    policy MUST NOT resolve users, tenants, or services.
    """
    assert_module_purity("policy")


def test_audit_is_explanation_only():
    """
    audit MUST NOT persist, log, or emit.
    """
    assert_module_purity("audit")


def test_registry_is_metadata_only():
    """
    registry MUST NOT make business or policy decisions.
    """
    assert_module_purity("registry")
