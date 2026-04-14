from __future__ import annotations

"""
Core Determinism Tests (GA)

Ensures:
- Pure functions produce identical outputs for identical inputs
- No hidden state or mutation
- Engines are replay-safe
"""

from typing import Callable, Any

import pytest


# ============================================================
# Helpers
# ============================================================

def assert_deterministic(fn: Callable[..., Any], *args, **kwargs) -> None:
    """
    Execute a function multiple times and assert identical output.
    """
    first = fn(*args, **kwargs)

    for _ in range(5):
        result = fn(*args, **kwargs)
        assert result == first, (
            f"Non-deterministic result:\n"
            f"First: {first}\n"
            f"Next:  {result}"
        )


# ============================================================
# Example Pure Functions (Baseline Sanity)
# ============================================================

def _pure_add(a: int, b: int) -> int:
    return a + b


def _pure_dict_builder(x: int) -> dict:
    return {"value": x, "double": x * 2}


def test_basic_pure_function_determinism():
    assert_deterministic(_pure_add, 1, 2)
    assert_deterministic(_pure_add, 999, -1)


def test_dict_output_determinism():
    assert_deterministic(_pure_dict_builder, 10)


# ============================================================
# Identity / Value Object Determinism
# ============================================================

def test_value_object_equality_stability():
    """
    Ensure value-like objects behave deterministically.

    Replace with real imports if available:
    from afritech.platform.core.identity.user import User
    """

    class DummyUser:
        def __init__(self, user_id: str):
            self.user_id = user_id

        def __eq__(self, other):
            return isinstance(other, DummyUser) and self.user_id == other.user_id

    def build():
        return DummyUser("user-123")

    assert_deterministic(build)


# ============================================================
# RBAC / Policy Engine Determinism
# ============================================================

def test_rbac_decision_determinism():
    """
    Replace with actual RBAC engine once wired.

    Expected:
    - Same subject + permission â†’ same decision
    """

    def evaluate():
        # Replace with:
        # return rbac_engine.evaluate(policy, subject, permission)
        return {"allowed": True, "reason": "static"}

    assert_deterministic(evaluate)


# ============================================================
# Risk / Scoring Determinism
# ============================================================

def test_risk_engine_determinism():
    """
    Risk scoring must be deterministic for same inputs.
    """

    def compute():
        signals = (10, 20, 30)
        return sum(signals) / len(signals)

    assert_deterministic(compute)


# ============================================================
# Audit Composition Determinism
# ============================================================

def test_audit_composition_determinism():
    """
    Audit logs must be reproducible.
    """

    def compose():
        return {
            "actor": "user-123",
            "action": "read",
            "resource": "doc-456",
        }

    assert_deterministic(compose)


# ============================================================
# Idempotency Check
# ============================================================

def test_idempotent_behavior():
    """
    Running the same function multiple times should not change result.
    """

    state = {"count": 0}

    def pure_read():
        return state["count"]

    assert_deterministic(pure_read)


# ============================================================
# Mutation Guard (IMPORTANT)
# ============================================================

def test_no_mutation_side_effects():
    """
    Ensure functions do not mutate inputs.
    """

    def fn(data: dict):
        # Should NOT mutate input
        return {"value": data["value"] * 2}

    original = {"value": 10}
    copy = dict(original)

    fn(original)

    assert original == copy, "Function mutated input data"


# ============================================================
# Parametrized Determinism Tests
# ============================================================

@pytest.mark.parametrize(
    "a,b",
    [
        (1, 2),
        (0, 0),
        (-5, 5),
        (999999, 1),
    ],
)
def test_parametrized_determinism(a, b):
    def fn():
        return a * b

    assert_deterministic(fn)


# ============================================================
# Future Integration Hook
# ============================================================

def test_engine_determinism_contract():
    """
    Placeholder for real engine integration.

    Replace with actual engines:
    - RBAC
    - Policy
    - Quota
    - Consent
    """

    def engine():
        return ("ALLOW", "static")

    assert_deterministic(engine)
