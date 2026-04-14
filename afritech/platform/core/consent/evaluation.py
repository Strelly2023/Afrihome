from __future__ import annotations

"""
GA Enterprise Core â€” Consent Evaluation
--------------------------------------

LAYER: L2 (Pure Engine)
Dependencies:
- core.consent.definition
- core.consent.snapshot
- core.consent.decision
- core.consent.errors

Deterministic: YES
Side effects: NONE
IO / Time / Network: NONE

Purpose:
- Evaluate whether processing is legally permitted under consent rules
- Produce a deterministic consent decision with explainable reasons

Rules:
- Pure evaluation only
- No clocks (time is injected as data)
- No persistence, mutation, or side effects
- Structural misuse MUST raise ConsentEvaluationError
- Legal allow/deny outcomes are DECISIONS, not errors
"""

from afritech.platform.core.consent.definition import ConsentDefinition
from afritech.platform.core.consent.snapshot import ConsentSnapshot
from afritech.platform.core.consent.decision import ConsentDecision
from afritech.platform.core.consent.errors import ConsentEvaluationError


class ConsentEvaluator:
    """
    Pure consent evaluation engine.

    Semantics:
    - Consent applies only if:
        * scope matches the definition
        * legal basis is acceptable
        * consent state is 'granted'
        * consent is not expired or revoked (as per snapshot and injected time)
    - Any violation results in deny (fail-safe)
    """

    def evaluate(
        self,
        *,
        definition: ConsentDefinition,
        snapshot: ConsentSnapshot,
        at_ms: int | None = None,
    ) -> ConsentDecision:
        """
        Evaluate consent legality.

        Args:
            definition:
                Immutable consent requirement definition.
            snapshot:
                Immutable snapshot of observed consent state.
            at_ms:
                Optional evaluation timestamp (milliseconds since epoch).
                Used only to compare against injected expiry/revocation data.

        Returns:
            ConsentDecision indicating allow/deny and reasons.

        Raises:
            ConsentEvaluationError for structurally invalid inputs.
        """

        # ----------------------------------------------------
        # Structural validation (fail-fast, deterministic)
        # ----------------------------------------------------

        if not isinstance(definition, ConsentDefinition):
            raise ConsentEvaluationError(
                consent_id="<unknown>",
                reason="definition must be a ConsentDefinition",
                metadata={"definition_type": type(definition).__name__},
            )

        if not isinstance(snapshot, ConsentSnapshot):
            raise ConsentEvaluationError(
                consent_id=definition.consent_id,
                reason="snapshot must be a ConsentSnapshot",
                metadata={"snapshot_type": type(snapshot).__name__},
            )

        if snapshot.consent_id != definition.consent_id:
            raise ConsentEvaluationError(
                consent_id=definition.consent_id,
                reason="snapshot.consent_id does not match definition.consent_id",
                metadata={
                    "definition_consent_id": definition.consent_id,
                    "snapshot_consent_id": snapshot.consent_id,
                },
            )

        # ----------------------------------------------------
        # Scope & legal basis checks (deny decision, not error)
        # ----------------------------------------------------

        if snapshot.scope not in definition.scopes:
            return ConsentDecision(
                allowed=False,
                state=snapshot.state,
                reasons=("scope_not_covered",),
            )

        if snapshot.legal_basis not in definition.legal_bases:
            return ConsentDecision(
                allowed=False,
                state=snapshot.state,
                reasons=("invalid_legal_basis",),
            )

        # ----------------------------------------------------
        # State evaluation (fail-safe)
        # ----------------------------------------------------

        if snapshot.state != "granted":
            return ConsentDecision(
                allowed=False,
                state=snapshot.state,
                reasons=("consent_not_granted",),
            )

        # ----------------------------------------------------
        # Temporal evaluation (data-driven)
        # ----------------------------------------------------

        if at_ms is not None:
            if not isinstance(at_ms, int) or at_ms < 0:
                raise ConsentEvaluationError(
                    consent_id=definition.consent_id,
                    reason="at_ms must be a non-negative integer if provided",
                    metadata={"at_ms": at_ms},
                )

            if (
                snapshot.expires_at_ms is not None
                and at_ms >= snapshot.expires_at_ms
            ):
                return ConsentDecision(
                    allowed=False,
                    state="expired",
                    reasons=("consent_expired",),
                )

            if snapshot.revoked_at_ms is not None:
                return ConsentDecision(
                    allowed=False,
                    state="revoked",
                    reasons=("consent_revoked",),
                )

        # ----------------------------------------------------
        # Final allow (NOT an error)
        # ----------------------------------------------------

        return ConsentDecision(
            allowed=True,
            state="granted",
            reasons=("consent_valid",),
        )


# ============================================================
# Consent Evaluator ABI (explicit, frozen)
# ============================================================

__all__ = [
    "ConsentEvaluator",
]
