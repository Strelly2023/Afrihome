"""
GA Core â€” Risk Property Tests
----------------------------

Purpose:
- Prove semantic correctness of the Risk engine
- Enforce deterministic and monotonic scoring behavior
- Guarantee replay-safe and explainable risk decisions

These tests validate PROPERTIES, not implementations.
"""

from afritech.platform.core.risk import (
    RiskSignal,
    RiskDefinition,
    RiskSnapshot,
    RiskEvaluator,
    SCORE_MIN,
    SCORE_MAX,
)


EVALUATOR = RiskEvaluator()


# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------

def eval_risk(
    *,
    definition: RiskDefinition,
    snapshot: RiskSnapshot,
):
    """
    Deterministically evaluate a risk decision.
    """
    return EVALUATOR.evaluate(
        definition=definition,
        snapshot=snapshot,
    )


# ------------------------------------------------------------
# Property 1 â€” Determinism
# ------------------------------------------------------------

def test_risk_determinism():
    """
    Identical inputs MUST produce identical outputs.
    """
    definition = RiskDefinition(
        model_id="test-risk",
        base_score=10,
        signals=(
            RiskSignal("geo_mismatch", weight=20),
        ),
        band_thresholds=(
            ("low", 0),
            ("medium", 30),
            ("high", 60),
            ("critical", 90),
        ),
    )

    snapshot = RiskSnapshot(
        model_id="test-risk",
        signals=(
            RiskSignal("geo_mismatch"),
        ),
    )

    d1 = eval_risk(definition=definition, snapshot=snapshot)
    d2 = eval_risk(definition=definition, snapshot=snapshot)
    d3 = eval_risk(definition=definition, snapshot=snapshot)

    assert d1 == d2 == d3


# ------------------------------------------------------------
# Property 2 â€” Signal contributes to score
# ------------------------------------------------------------

def test_signal_contribution_increases_score():
    """
    A matching signal must increase the total risk score.
    """
    definition = RiskDefinition(
        model_id="risk-2",
        base_score=10,
        signals=(
            RiskSignal("velocity_spike", weight=25),
        ),
        band_thresholds=(
            ("low", 0),
            ("medium", 20),
            ("high", 50),
            ("critical", 80),
        ),
    )

    snapshot = RiskSnapshot(
        model_id="risk-2",
        signals=(
            RiskSignal("velocity_spike"),
        ),
    )

    decision = eval_risk(definition=definition, snapshot=snapshot)

    assert decision.score == 35
    assert "velocity_spike" in decision.reasons


# ------------------------------------------------------------
# Property 3 â€” Band resolution is correct
# ------------------------------------------------------------

def test_band_resolution():
    """
    Risk band must be resolved according to thresholds.
    """
    definition = RiskDefinition(
        model_id="risk-band",
        base_score=40,
        signals=(
            RiskSignal("anomaly_detected", weight=30),
        ),
        band_thresholds=(
            ("low", 0),
            ("medium", 20),
            ("high", 60),
            ("critical", 90),
        ),
    )

    snapshot = RiskSnapshot(
        model_id="risk-band",
        signals=(
            RiskSignal("anomaly_detected"),
        ),
    )

    decision = eval_risk(definition=definition, snapshot=snapshot)

    assert decision.score == 70
    assert decision.band == "high"


# ------------------------------------------------------------
# Property 4 â€” Monotonic scoring
# ------------------------------------------------------------

def test_monotonic_score_increase():
    """
    Adding signals must never reduce the risk score.
    """
    definition = RiskDefinition(
        model_id="risk-mono",
        base_score=10,
        signals=(
            RiskSignal("geo_mismatch", weight=10),
            RiskSignal("velocity_spike", weight=20),
        ),
        band_thresholds=(
            ("low", 0),
            ("medium", 15),
            ("high", 40),
            ("critical", 70),
        ),
    )

    snapshot_1 = RiskSnapshot(
        model_id="risk-mono",
        signals=(
            RiskSignal("geo_mismatch"),
        ),
    )

    snapshot_2 = RiskSnapshot(
        model_id="risk-mono",
        signals=(
            RiskSignal("geo_mismatch"),
            RiskSignal("velocity_spike"),
        ),
    )

    d1 = eval_risk(definition=definition, snapshot=snapshot_1)
    d2 = eval_risk(definition=definition, snapshot=snapshot_2)

    assert d2.score > d1.score


# ------------------------------------------------------------
# Property 5 â€” Score clamping
# ------------------------------------------------------------

def test_risk_score_clamped():
    """
    Risk score must be clamped between SCORE_MIN and SCORE_MAX.
    """
    definition = RiskDefinition(
        model_id="clamp",
        base_score=90,
        signals=(
            RiskSignal("geo_mismatch", weight=50),  # âœ… valid grammar signal
        ),
        band_thresholds=(
            ("low", 0),
            ("high", 80),
            ("critical", 95),
        ),
    )

    snapshot = RiskSnapshot(
        model_id="clamp",
        signals=(
            RiskSignal("geo_mismatch"),
        ),
    )

    decision = eval_risk(definition=definition, snapshot=snapshot)

    assert SCORE_MIN <= decision.score <= SCORE_MAX


# ------------------------------------------------------------
# Property 6 â€” Replay safety
# ------------------------------------------------------------

def test_replay_safety():
    """
    Repeated evaluation must yield identical results.
    """
    definition = RiskDefinition(
        model_id="replay",
        base_score=5,
        signals=(
            RiskSignal("untrusted_device", weight=15),
        ),
        band_thresholds=(
            ("low", 0),
            ("medium", 10),
            ("high", 30),
        ),
    )

    snapshot = RiskSnapshot(
        model_id="replay",
        signals=(
            RiskSignal("untrusted_device"),
        ),
    )

    results = [
        eval_risk(definition=definition, snapshot=snapshot)
        for _ in range(5)
    ]

    assert all(r == results[0] for r in results)
