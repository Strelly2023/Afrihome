"""
DEC-001 — Pipeline Order Invariant

Law:
    Decision engines MUST execute in the exact order declared
    by the governance definition.

Rationale:
    - Deterministic decision behavior
    - Predictable audit traces
    - Valid composition of independent engines

Enforcement:
    Tool-based (pipeline_guard) + test-based validation
"""

from typing import List


# ---------------------------------------------------------------------
# Test doubles
# ---------------------------------------------------------------------

class RecordingEngine:
    """
    Simple engine that records execution order.
    """
    def __init__(self, name: str, recorder: List[str]):
        self.name = name
        self.recorder = recorder

    def evaluate(self):
        self.recorder.append(self.name)
        return None


# ---------------------------------------------------------------------
# Canonical pipeline executor
# (replace with the real system executor if/when available)
# ---------------------------------------------------------------------

def execute_pipeline(engines: List[RecordingEngine]):
    """
    Execute all engines in the given order.
    """
    for engine in engines:
        engine.evaluate()


# ---------------------------------------------------------------------
# DEC-001 Tests — Pipeline Order
# ---------------------------------------------------------------------

def test_pipeline_executes_in_declared_order():
    executed: List[str] = []

    engines = [
        RecordingEngine("rbac", executed),
        RecordingEngine("policy", executed),
        RecordingEngine("quota", executed),
        RecordingEngine("risk", executed),
        RecordingEngine("consent", executed),
    ]

    execute_pipeline(engines)

    assert executed == [
        "rbac",
        "policy",
        "quota",
        "risk",
        "consent",
    ], "Pipeline did not execute in the declared order"


def test_pipeline_order_violation_is_detectable():
    """
    This test intentionally executes engines in the wrong order
    to prove that order matters and is observable.

    It documents the failure mode, even though enforcement
    is handled by pipeline_guard.
    """
    executed: List[str] = []

    engines = [
        RecordingEngine("policy", executed),   # ❌ wrong order
        RecordingEngine("rbac", executed),
        RecordingEngine("quota", executed),
        RecordingEngine("risk", executed),
        RecordingEngine("consent", executed),
    ]

    execute_pipeline(engines)

    assert executed != [
        "rbac",
        "policy",
        "quota",
        "risk",
        "consent",
    ], "Order violation was not detectable"


def test_single_engine_pipeline_is_valid():
    executed: List[str] = []

    engines = [
        RecordingEngine("rbac", executed),
    ]

    execute_pipeline(engines)

    assert executed == ["rbac"]


def test_empty_pipeline_is_valid_and_does_nothing():
    executed: List[str] = []

    engines: List[RecordingEngine] = []

    execute_pipeline(engines)

    assert executed == []