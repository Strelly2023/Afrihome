from __future__ import annotations

"""
GA Enterprise Core â€” Audit Composer
----------------------------------

LAYER: L2 (Pure Projection Engine)
Dependencies:
- core.audit.decision
- core.audit.trace
- core.typing.enums
- core.audit.errors
- stdlib only

Deterministic: YES
Side effects: NONE
IO / Time / Network: NONE

Purpose:
- Compose a final AuditDecision from RBAC and Policy outcomes
- Produce a single, immutable, replay-safe audit artifact

Rules:
- Pure composition only
- NO IO, persistence, or verification logic
- NO identity, tenancy, or execution context awareness
- NO semantic authority (projection only)

Any change requires an ADR.
"""

from typing import Tuple

from afritech.platform.core.audit.decision import AuditDecision
from afritech.platform.core.audit.trace import AuditTrace
from afritech.platform.core.audit.errors import AuditCompositionError
from afritech.platform.core.typing.enums import (
    EngineId,
    DecisionVerdictType,
)


# ============================================================
# Audit Composer (pure, deterministic projection)
# ============================================================

class AuditComposer:
    """
    Pure composer of audit facts.

    This class combines:
    - RBAC outcome
    - Policy outcome
    - Their associated factual traces

    Into a single, immutable AuditDecision that
    *faithfully projects* core decision semantics.
    """

    def compose(
        self,
        *,
        rbac_allowed: bool,
        policy_allowed: bool,
        rbac_traces: Tuple[AuditTrace, ...] = (),
        policy_traces: Tuple[AuditTrace, ...] = (),
    ) -> AuditDecision:
        """
        Compose a final AuditDecision from RBAC and Policy outcomes.

        Args:
            rbac_allowed:
                Result of RBAC evaluation.
            policy_allowed:
                Result of Policy evaluation.
            rbac_traces:
                Factual traces produced by RBAC evaluation.
            policy_traces:
                Factual traces produced by Policy evaluation.

        Returns:
            A single immutable AuditDecision representing the
            combined authorization outcome.

        Raises:
            AuditCompositionError if inputs are structurally invalid.
        """

        # -----------------------------------------------------
        # Structural validation (fail-fast, deterministic)
        # -----------------------------------------------------

        if not isinstance(rbac_allowed, bool):
            raise AuditCompositionError("rbac_allowed must be a boolean")

        if not isinstance(policy_allowed, bool):
            raise AuditCompositionError("policy_allowed must be a boolean")

        if not isinstance(rbac_traces, tuple):
            raise AuditCompositionError("rbac_traces must be a tuple")

        if not isinstance(policy_traces, tuple):
            raise AuditCompositionError("policy_traces must be a tuple")

        if any(not isinstance(t, AuditTrace) for t in rbac_traces):
            raise AuditCompositionError(
                "all rbac_traces must be AuditTrace instances"
            )

        if any(not isinstance(t, AuditTrace) for t in policy_traces):
            raise AuditCompositionError(
                "all policy_traces must be AuditTrace instances"
            )

        # -----------------------------------------------------
        # Canonical decision semantics (deny-wins)
        # -----------------------------------------------------

        allowed = rbac_allowed and policy_allowed
        verdict = (
            DecisionVerdictType.ALLOW
            if allowed
            else DecisionVerdictType.DENY
        )

        # -----------------------------------------------------
        # Deterministic trace composition
        # -----------------------------------------------------

        combined_traces = rbac_traces + policy_traces

        # -----------------------------------------------------
        # Final audit projection
        # -----------------------------------------------------

        return AuditDecision(
            allowed=allowed,
            verdict=verdict,
            engine=EngineId.COMBINED,
            reason=verdict.value,
            traces=combined_traces,
        )


# ============================================================
# Audit Composer ABI (explicit, frozen)
# ============================================================

__all__ = [
    "AuditComposer",
]
