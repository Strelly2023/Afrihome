"""
DEC-004 — No Short-Circuit Invariant

Law:
    All decision engines in the pipeline MUST execute,
    regardless of intermediate ALLOW or DENY results.

Rationale:
    - Audit completeness
    - Deterministic decision traces
    - No hidden side effects
    - Separation of evaluation and combination

Enforcement:
    Test-based (TEST_ONLY_RULE)
"""

from typing import List


# ---------------------------------------------------------------------
# Test Doubles (Minimal, Explicit)
# ---------------------------------------------------------------------

class DecisionOutcome:
    ALLOW = "ALLOW"
    DENY = "DENY"
    ABSTAIN = "ABSTAIN"


class FakeEngine:
    """
    Minimal engine that records execution.
    """
    def __init__(self, outcome: str, recorder: List[str], name: str):
        self.outcome = outcome
        self.recorder = recorder
        self.name = name

    def evaluate(self):
        self.recorder.append(self.name)
        return self.outcome


# ---------------------------------------------------------------------
# Canonical evaluation loop (replace with real pipeline if available)
# ---------------------------------------------------------------------

def evaluate_pipeline(engines: List[FakeEngine]):
    """
    Correct behavior:
        - Call evaluate() on ALL engines
        - Collect outcomes
        - Do NOT early-return
    """
    outcomes = []
    for engine in engines:
        outcome = engine.evaluate()
        outcomes.append(outcome)
    return outcomes


# ---------------------------------------------------------------------
# DEC-004 Tests — No Short Circuit
# ---------------------------------------------------------------------

def test_pipeline_does_not_short_circuit_on_deny():
    executed = []

    engines = [
        FakeEngine(DecisionOutcome.DENY, executed, "engine_1"),
        FakeEngine(DecisionOutcome.ALLOW, executed, "engine_2"),
        FakeEngine(DecisionOutcome.ABSTAIN, executed, "engine_3"),
    ]

    evaluate_pipeline(engines)

    assert executed == [
        "engine_1",
        "engine_2",
        "engine_3",
    ], "Pipeline short-circuited execution"


def test_pipeline_does_not_short_circuit_on_allow():
    executed = []

    engines = [
        FakeEngine(DecisionOutcome.ALLOW, executed, "engine_1"),
        FakeEngine(DecisionOutcome.DENY, executed, "engine_2"),
        FakeEngine(DecisionOutcome.ABSTAIN, executed, "engine_3"),
    ]

    evaluate_pipeline(engines)

    assert executed == [
        "engine_1",
        "engine_2",
        "engine_3",
    ], "Pipeline short-circuited execution"


def test_pipeline_executes_all_engines_even_if_all_deny():
    executed = []

    engines = [
        FakeEngine(DecisionOutcome.DENY, executed, "engine_1"),
        FakeEngine(DecisionOutcome.DENY, executed, "engine_2"),
        FakeEngine(DecisionOutcome.DENY, executed, "engine_3"),
    ]

    evaluate_pipeline(engines)

    assert executed == [
        "engine_1",
        "engine_2",
        "engine_3",
    ], "Pipeline short-circuited execution"


def test_empty_pipeline_executes_nothing_but_is_valid():
    executed = []

    engines = []

    outcomes = evaluate_pipeline(engines)

    assert outcomes == []
    assert executed == []
