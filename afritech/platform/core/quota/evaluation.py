from __future__ import annotations

"""
GA Enterprise Core â€” Quota Evaluation
------------------------------------

LAYER: L2 (Pure Engine)
Dependencies:
- core.quota.definition
- core.quota.snapshot
- core.quota.decision
- core.quota.errors

Deterministic: YES
Side effects: NONE
IO / Time / Network: NONE

Purpose:
- Evaluate a quota definition against a usage snapshot
- Produce a deterministic allow/deny quota decision

Rules:
- Pure evaluation only
- No clocks, persistence, or mutation
- Fail-safe, deny-wins semantics
- Structural misuse MUST raise QuotaEvaluationError
- Quota exhaustion is a DECISION, not an error
"""

from afritech.platform.core.quota.definition import QuotaDefinition
from afritech.platform.core.quota.snapshot import QuotaSnapshot
from afritech.platform.core.quota.decision import QuotaDecision
from afritech.platform.core.quota.errors import QuotaEvaluationError


class QuotaEvaluator:
    """
    Pure quota evaluation engine.

    Evaluates whether a single action is permitted
    under a given quota definition and usage snapshot.
    """

    def evaluate(
        self,
        *,
        definition: QuotaDefinition,
        snapshot: QuotaSnapshot,
        cost: int = 1,
    ) -> QuotaDecision:
        """
        Evaluate a quota decision.

        Args:
            definition:
                Immutable quota definition.
            snapshot:
                Immutable usage snapshot.
            cost:
                Cost of the attempted action (defaults to 1 unit).

        Returns:
            QuotaDecision describing allow/deny outcome.

        Raises:
            QuotaEvaluationError for structurally invalid inputs.
        """

        # --------------------------------------------------
        # Structural validation (fail-fast, deterministic)
        # --------------------------------------------------

        if not isinstance(definition, QuotaDefinition):
            raise QuotaEvaluationError(
                quota_id="<unknown>",
                reason="definition must be a QuotaDefinition",
                metadata={"definition_type": type(definition).__name__},
            )

        if not isinstance(snapshot, QuotaSnapshot):
            raise QuotaEvaluationError(
                quota_id=definition.quota_id,
                reason="snapshot must be a QuotaSnapshot",
                metadata={"snapshot_type": type(snapshot).__name__},
            )

        if not isinstance(cost, int) or cost <= 0:
            raise QuotaEvaluationError(
                quota_id=definition.quota_id,
                reason="cost must be a positive integer",
                metadata={"cost": cost},
            )

        if snapshot.quota_id != definition.quota_id:
            raise QuotaEvaluationError(
                quota_id=definition.quota_id,
                reason="snapshot.quota_id does not match definition.quota_id",
                metadata={
                    "definition_quota_id": definition.quota_id,
                    "snapshot_quota_id": snapshot.quota_id,
                },
            )

        # --------------------------------------------------
        # Pure evaluation logic (deny-wins)
        # --------------------------------------------------

        used_after = snapshot.used + cost
        limit = definition.limit

        remaining = max(limit - used_after, 0)

        if used_after > limit:
            # IMPORTANT:
            # Limit exhaustion is NOT an error.
            # It is a legitimate deny decision.
            return QuotaDecision(
                allowed=False,
                reason="deny: limit_exceeded",
                limit=limit,
                used=used_after,
                remaining=remaining,
            )

        return QuotaDecision(
            allowed=True,
            reason="allow",
            limit=limit,
            used=used_after,
            remaining=remaining,
        )


# ============================================================
# Quota Evaluator ABI (explicit, frozen)
# ============================================================

__all__ = [
    "QuotaEvaluator",
]
