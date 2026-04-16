"""
Guard registry.

This module defines the *authoritative mapping* between rule types
(declared in rules/*.yaml) and enforcement mechanisms.

Rules fall into two categories:
1. Tool-enforced rules  → mapped to a guard implementation
2. Test-only rules      → enforced exclusively via tests

If a rule type is neither mapped nor declared test-only,
governance MUST fail loudly.
"""

from afritech.tools import import_guard, ast_guard

# ---------------------------------------------------------------------
# Tool-enforced rules
# ---------------------------------------------------------------------
#
# Mapping: rule_type -> guard module
#
# Each guard module MUST expose:
#     run(rule: dict, context: dict) -> GuardResult
#

TOOL_MAP = {
    # ---------------------------------------------------------------
    # Core / structural rules
    # ---------------------------------------------------------------
    "forbidden_import": import_guard,

    # ---------------------------------------------------------------
    # Semantic rules (AST-based)
    # ---------------------------------------------------------------
    "forbidden_call": ast_guard,    # CORE-004
    "no_global_state": ast_guard,   # CORE-007

    # ---------------------------------------------------------------
    # NOTE:
    # DEC-001 (pipeline_order) is intentionally NOT tool-enforced yet.
    # It is enforced via constitutional tests until pipeline wiring
    # is connected to the executor.
    # ---------------------------------------------------------------
}

# ---------------------------------------------------------------------
# Test-only rules
# ---------------------------------------------------------------------
#
# These rules are real laws, but are enforced via invariant tests
# rather than static tooling (for now).
#
# They MUST be explicitly declared here to preserve META-002:
# "Every rule must have a declared enforcement mechanism."
#

TEST_ONLY_RULES = {
    # ---------------------------------------------------------------
    # Decision semantics
    # ---------------------------------------------------------------
    "deny_wins",
    "no_short_circuit",
    "typed_outcome",

    # ---------------------------------------------------------------
    # Decision structure (TEMPORARY)
    # ---------------------------------------------------------------
    "pipeline_order",   # ✅ DEC-001 enforced by tests for now

    # ---------------------------------------------------------------
    # Determinism / behavioral guarantees
    # ---------------------------------------------------------------
    "deterministic_output",

    # ---------------------------------------------------------------
    # Domain integrity (future static enforcement)
    # ---------------------------------------------------------------
    "type_guard",
    "immutability",
    "explicit_mapping",
    "boundary_guard",

    # ---------------------------------------------------------------
    # System-level structural guarantees
    # ---------------------------------------------------------------
    "no_cycles",
}

# ---------------------------------------------------------------------
# Public helpers
# ---------------------------------------------------------------------

def is_test_only(rule_type: str) -> bool:
    """
    Return True if the given rule type is enforced exclusively via tests.

    Test-only rules are:
    - Loaded and validated
    - Accounted for in governance completeness
    - Skipped during static tool execution

    They MUST still have invariant tests.
    """
    return rule_type in TEST_ONLY_RULES