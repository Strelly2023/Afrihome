"""
GA Core â€” Quota Property Tests
-----------------------------

Purpose:
- Prove semantic correctness of the Quota engine
- Enforce deny-wins and deterministic behavior
- Guarantee replay-safe quota evaluation

These tests validate PROPERTIES, not implementations.
"""

from afritech.platform.core.quota import (
    QuotaDefinition,
    QuotaSnapshot,
    QuotaEvaluator,
)


EVALUATOR = QuotaEvaluator()


# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------

def eval_quota(
    *,
    definition: QuotaDefinition,
    snapshot: QuotaSnapshot,
    cost: int = 1,
):
    """
    Deterministically evaluate a quota decision.
    """
    return EVALUATOR.evaluate(
        definition=definition,
        snapshot=snapshot,
        cost=cost,
    )


# ------------------------------------------------------------
# Property 1 â€” Allow under limit
# ------------------------------------------------------------

def test_allow_when_under_limit():
    """
    Requests below the quota limit must be allowed.
    """
    definition = QuotaDefinition(
        quota_id="api-requests",
        unit="requests",
        scope="tenant",
        dimension="total",
        limit=100,
    )

    snapshot = QuotaSnapshot(
        quota_id="api-requests",
        used=10,
        remaining=90,
    )

    decision = eval_quota(
        definition=definition,
        snapshot=snapshot,
        cost=1,
    )

    assert decision.allowed is True
    assert decision.reason == "allow"
    assert decision.remaining == 89


# ------------------------------------------------------------
# Property 2 â€” Deny when quota exhausted
# ------------------------------------------------------------

def test_deny_when_limit_exceeded():
    """
    Requests that exceed remaining quota must be denied.
    """
    definition = QuotaDefinition(
        quota_id="api-requests",
        unit="requests",
        scope="tenant",
        dimension="total",
        limit=10,
    )

    snapshot = QuotaSnapshot(
        quota_id="api-requests",
        used=10,
        remaining=0,
    )

    decision = eval_quota(
        definition=definition,
        snapshot=snapshot,
        cost=1,
    )

    assert decision.allowed is False
    assert decision.reason.startswith("deny")
    assert decision.remaining == 0


# ------------------------------------------------------------
# Property 3 â€” Cost is applied correctly
# ------------------------------------------------------------

def test_cost_handling():
    """
    Cost must be subtracted deterministically from remaining quota.
    """
    definition = QuotaDefinition(
        quota_id="data-bytes",
        unit="bytes",
        scope="service",
        dimension="total",
        limit=1000,
    )

    snapshot = QuotaSnapshot(
        quota_id="data-bytes",
        used=900,
        remaining=100,
    )

    decision = eval_quota(
        definition=definition,
        snapshot=snapshot,
        cost=50,
    )

    assert decision.allowed is True
    assert decision.remaining == 50


# ------------------------------------------------------------
# Property 4 â€” Deny-wins at boundary
# ------------------------------------------------------------

def test_deny_wins_exact_boundary():
    """
    When cost exceeds remaining quota, deny must win.
    Remaining reflects evaluated post-cost capacity (clamped),
    not the original snapshot value.
    """
    definition = QuotaDefinition(
        quota_id="ops",
        unit="operations",
        scope="user",
        dimension="total",
        limit=10,
    )

    snapshot = QuotaSnapshot(
        quota_id="ops",
        used=9,
        remaining=1,
    )

    decision = eval_quota(
        definition=definition,
        snapshot=snapshot,
        cost=2,
    )

    assert decision.allowed is False
    assert decision.reason.startswith("deny")
    assert decision.remaining == 0


# ------------------------------------------------------------
# Property 5 â€” Determinism / idempotence
# ------------------------------------------------------------

def test_quota_determinism():
    """
    Identical inputs MUST always produce identical outputs.
    """
    definition = QuotaDefinition(
        quota_id="emails",
        unit="messages",
        scope="service",
        dimension="total",
        limit=5,
    )

    snapshot = QuotaSnapshot(
        quota_id="emails",
        used=2,
        remaining=3,
    )

    d1 = eval_quota(
        definition=definition,
        snapshot=snapshot,
        cost=1,
    )

    d2 = eval_quota(
        definition=definition,
        snapshot=snapshot,
        cost=1,
    )

    d3 = eval_quota(
        definition=definition,
        snapshot=snapshot,
        cost=1,
    )

    assert d1 == d2 == d3


# ------------------------------------------------------------
# Property 6 â€” No mutation of inputs
# ------------------------------------------------------------

def test_quota_does_not_mutate_snapshot():
    """
    Quota evaluation must not mutate the input snapshot.
    """
    definition = QuotaDefinition(
        quota_id="events",
        unit="requests",  # valid grammar unit
        scope="tenant",
        dimension="total",
        limit=10,
    )

    snapshot = QuotaSnapshot(
        quota_id="events",
        used=3,
        remaining=7,
    )

    snapshot_copy = QuotaSnapshot(
        quota_id=snapshot.quota_id,
        used=snapshot.used,
        remaining=snapshot.remaining,
    )

    _ = eval_quota(
        definition=definition,
        snapshot=snapshot,
        cost=2,
    )

    # Snapshot must remain unchanged
    assert snapshot == snapshot_copy
