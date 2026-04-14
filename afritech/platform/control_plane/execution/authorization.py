from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Tuple

from afritech.platform.core.decision import Decision
from afritech.platform.core.decision.engine_outcome import EngineOutcome
from afritech.platform.core.decision.reason import DecisionReason
from afritech.platform.core.typing.enums import EngineId, DecisionVerdictType

from afritech.platform.control_plane.audit.models import ExecutionAuditRecord
from afritech.platform.control_plane.audit.sink import ExecutionAuditSink


# ---------------------------------------------------------------------
# Helpers (Execution-layer reason factory)
# ---------------------------------------------------------------------

def execution_reason(code: str) -> DecisionReason:
    return DecisionReason(
        engine=EngineId.COMBINED,
        code=code,
        metadata={},
    )


# ---------------------------------------------------------------------
# Execution Context & Result
# ---------------------------------------------------------------------

@dataclass(frozen=True)
class ExecutionContext:
    actor: str
    action: str
    resource: str
    environment: str | None = None


@dataclass(frozen=True)
class AuthorizedAction:
    actor: str
    action: str
    resource: str
    reasons: Tuple[DecisionReason, ...]


# ---------------------------------------------------------------------
# Execution Errors
# ---------------------------------------------------------------------

class AuthorizationError(Exception):
    def __init__(self, reasons: Tuple[DecisionReason, ...]):
        super().__init__(str(reasons))
        self.reasons = reasons


class AuthorizationDenied(AuthorizationError):
    pass


class AuthorizationConditional(AuthorizationError):
    pass


class AuthorityNotGranted(AuthorizationError):
    pass


class UnexplainableDecision(AuthorizationError):
    pass


class MissingDecision(AuthorizationError):
    pass


# ---------------------------------------------------------------------
# AuthorizeActionHandler (WITH AUDIT BINDING)
# ---------------------------------------------------------------------

class AuthorizeActionHandler:
    """
    Execution-layer authorization gate with audit binding.

    ❗ Execution WITHOUT audit is forbidden.
    """

    def __init__(self, *, audit_sink: ExecutionAuditSink) -> None:
        self._audit_sink = audit_sink

    def authorize(
        self,
        *,
        decision: Decision | None,
        outcomes: Tuple[EngineOutcome, ...],
        context: ExecutionContext,
    ) -> AuthorizedAction:

        # --------------------------------------------------------------
        # 0. Decision Presence (Fail-Closed)
        # --------------------------------------------------------------

        if decision is None:
            raise MissingDecision(
                (execution_reason("execution.missing_decision"),)
            )

        if not outcomes:
            raise AuthorizationDenied(
                (execution_reason("execution.missing_outcomes"),)
            )

        # --------------------------------------------------------------
        # 1. Verdict Enforcement
        # --------------------------------------------------------------

        if decision.verdict == DecisionVerdictType.DENY:
            raise AuthorizationDenied(decision.reasons)

        if decision.verdict == DecisionVerdictType.CONDITIONAL:
            raise AuthorizationConditional(decision.reasons)

        if decision.verdict != DecisionVerdictType.ALLOW:
            raise AuthorizationDenied(
                (execution_reason("execution.unknown_verdict"),)
            )

        # --------------------------------------------------------------
        # 2. Authority Isolation (RBAC only)
        # --------------------------------------------------------------

        rbac_outcomes = tuple(
            o for o in outcomes if o.engine == EngineId.RBAC
        )

        if not rbac_outcomes:
            raise AuthorityNotGranted(
                (execution_reason("execution.missing_rbac_evaluation"),)
            )

        if not any(o.verdict == DecisionVerdictType.ALLOW for o in rbac_outcomes):
            raise AuthorityNotGranted(
                (execution_reason("execution.rbac_not_granted"),)
            )

        # --------------------------------------------------------------
        # 3. Explainability Enforcement
        # --------------------------------------------------------------

        if not decision.reasons:
            raise UnexplainableDecision(
                (execution_reason("execution.missing_explanation"),)
            )

        # --------------------------------------------------------------
        # 4. EXECUTION AUDIT BINDING (NON-BYPASSABLE)
        # --------------------------------------------------------------

        audit_record = ExecutionAuditRecord(
            decision_id=str(id(decision)),
            actor=context.actor,
            action=context.action,
            resource=context.resource,
            reasons=decision.reasons,
            timestamp=datetime.utcnow(),
        )

        # ❗ Fail-closed: if audit fails, execution must fail
        self._audit_sink.record(audit_record)

        # --------------------------------------------------------------
        # 5. Successful Authorization
        # --------------------------------------------------------------

        return AuthorizedAction(
            actor=context.actor,
            action=context.action,
            resource=context.resource,
            reasons=decision.reasons,
        )
