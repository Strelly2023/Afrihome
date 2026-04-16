import pytest


# ---------------------------------------------------------------------
# Minimal DecisionOutcome abstraction
# (replace import with real one if it exists)
# ---------------------------------------------------------------------

class DecisionOutcome:
    ALLOW = "ALLOW"
    DENY = "DENY"
    ABSTAIN = "ABSTAIN"


# ---------------------------------------------------------------------
# Canonical combinator behavior (replace with real function if exists)
# ---------------------------------------------------------------------

def combine_decisions(outcomes):
    """
    Canonical decision combinator.

    LAW (DEC-002):
    - If ANY outcome is DENY → final is DENY
    - Else if at least one ALLOW → final is ALLOW
    - Else → ABSTAIN
    """
    if DecisionOutcome.DENY in outcomes:
        return DecisionOutcome.DENY

    if DecisionOutcome.ALLOW in outcomes:
        return DecisionOutcome.ALLOW

    return DecisionOutcome.ABSTAIN


# ---------------------------------------------------------------------
# DEC‑002 Tests — Deny Wins
# ---------------------------------------------------------------------

def test_single_deny_overrides_allow():
    outcomes = [
        DecisionOutcome.ALLOW,
        DecisionOutcome.DENY,
    ]

    result = combine_decisions(outcomes)

    assert result == DecisionOutcome.DENY


def test_multiple_allows_and_one_deny():
    outcomes = [
        DecisionOutcome.ALLOW,
        DecisionOutcome.ALLOW,
        DecisionOutcome.ALLOW,
        DecisionOutcome.DENY,
    ]

    result = combine_decisions(outcomes)

    assert result == DecisionOutcome.DENY


def test_deny_only():
    outcomes = [DecisionOutcome.DENY]

    result = combine_decisions(outcomes)

    assert result == DecisionOutcome.DENY


def test_deny_and_abstain():
    outcomes = [
        DecisionOutcome.ABSTAIN,
        DecisionOutcome.DENY,
        DecisionOutcome.ABSTAIN,
    ]

    result = combine_decisions(outcomes)

    assert result == DecisionOutcome.DENY


def test_allows_without_deny():
    outcomes = [
        DecisionOutcome.ALLOW,
        DecisionOutcome.ALLOW,
    ]

    result = combine_decisions(outcomes)

    assert result == DecisionOutcome.ALLOW


def test_all_abstain_results_in_abstain():
    outcomes = [
        DecisionOutcome.ABSTAIN,
        DecisionOutcome.ABSTAIN,
    ]

    result = combine_decisions(outcomes)

    assert result == DecisionOutcome.ABSTAIN


def test_empty_outcomes_defaults_to_abstain():
    outcomes = []

    result = combine_decisions(outcomes)

    assert result == DecisionOutcome.ABSTAIN