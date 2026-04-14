from __future__ import annotations

"""
GA Enterprise Core â€” Risk Evaluation
-----------------------------------

LAYER: L2 (Pure Engine)
Dependencies:
- core.risk.definition
- core.risk.snapshot
- core.risk.decision
- core.risk.errors
- core.risk.grammar

Deterministic: YES
Side effects: NONE
IO / Time / Network: NONE

Purpose:
- Evaluate a risk definition against a risk snapshot
- Produce a deterministic risk score and band

Rules:
- Pure evaluation only
- No clocks, persistence, IO, or mutation
- Deterministic, replay-safe semantics
- Structural misuse MUST raise RiskEvaluationError
- Risk severity (high/critical) is a DECISION, not an error
"""

from afritech.platform.core.risk.definition import RiskDefinition
from afritech.platform.core.risk.snapshot import RiskSnapshot
from afritech.platform.core.risk.decision import RiskDecision
from afritech.platform.core.risk.errors import RiskEvaluationError
from afritech.platform.core.risk.grammar import (
    SCORE_MIN,
    SCORE_MAX,
)


class RiskEvaluator:
    """
    Pure risk evaluation engine.

    Semantics:
    - Start from the base_score defined in the model
    - For each observed signal present in the definition,
      add its deterministic weight (if any)
    - Clamp the resulting score to the canonical score range
    - Map the score to a band using ordered band thresholds
    """

    def evaluate(
        self,
        *,
        definition: RiskDefinition,
        snapshot: RiskSnapshot,
    ) -> RiskDecision:
        """
        Evaluate risk for the given definition and snapshot.

        Args:
            definition:
                Immutable risk scoring definition.
            snapshot:
                Immutable snapshot of observed risk signals.

        Returns:
            RiskDecision containing final score, band, and reasons.

        Raises:
            RiskEvaluationError for structurally invalid inputs.
        """

        # ----------------------------------------------------
        # Structural validation (fail-fast, deterministic)
        # ----------------------------------------------------

        if not isinstance(definition, RiskDefinition):
            raise RiskEvaluationError(
                model_id="<unknown>",
                reason="definition must be a RiskDefinition",
                metadata={"definition_type": type(definition).__name__},
            )

        if not isinstance(snapshot, RiskSnapshot):
            raise RiskEvaluationError(
                model_id=definition.model_id,
                reason="snapshot must be a RiskSnapshot",
                metadata={"snapshot_type": type(snapshot).__name__},
            )

        if snapshot.model_id != definition.model_id:
            raise RiskEvaluationError(
                model_id=definition.model_id,
                reason="snapshot.model_id does not match definition.model_id",
                metadata={
                    "definition_model_id": definition.model_id,
                    "snapshot_model_id": snapshot.model_id,
                },
            )

        # ----------------------------------------------------
        # Scoring logic (pure, deterministic)
        # ----------------------------------------------------

        score = definition.base_score
        reasons: list[str] = []

        # Build lookup of signal weights by name
        weights = {
            signal.name: signal.weight
            for signal in definition.signals
            if signal.weight is not None
        }

        for signal in snapshot.signals:
            if signal.name in weights:
                score += weights[signal.name]
                reasons.append(signal.name)

        # ----------------------------------------------------
        # Clamp score to canonical range
        # ----------------------------------------------------

        if score < SCORE_MIN:
            score = SCORE_MIN
        elif score > SCORE_MAX:
            score = SCORE_MAX

        # ----------------------------------------------------
        # Band resolution (ordered thresholds)
        # ----------------------------------------------------

        band: str | None = None
        for band_name, threshold in definition.band_thresholds:
            if score >= threshold:
                band = band_name

        if band is None:
            # Defensive fallback: unreachable if definition is valid
            raise RiskEvaluationError(
                model_id=definition.model_id,
                reason="unable to resolve risk band",
                metadata={
                    "score": score,
                    "thresholds": definition.band_thresholds,
                },
            )

        # ----------------------------------------------------
        # Final decision (NOT an error)
        # ----------------------------------------------------

        return RiskDecision(
            score=score,
            band=band,
            reasons=tuple(reasons),
        )


# ============================================================
# Risk Evaluator ABI (explicit, frozen)
# ============================================================

__all__ = [
    "RiskEvaluator",
]
