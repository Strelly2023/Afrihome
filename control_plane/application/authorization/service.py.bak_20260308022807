from dataclasses import dataclass
from typing import Iterable, Tuple
from core.kernel.invariants import assert_not_none
from core.errors import AuthorizationError, GrammarViolationError
from core.rbac.policy_engine import evaluate as rbac_evaluate  # deny-wins engine
from core.rbac.grammar import validate_permission_name
from core.typing import Permission, RoleName
from control_plane.application.actors.service import ActorService
from control_plane.application.execution.models import ExecutionFrame
from .models import AccessDecision, DecisionStage
from .policies import PolicyProvider, GovernancePolicy

@dataclass(frozen=True, slots=True)
class AuthorizationService:
    """
    Orchestrates access decisions (deterministic, no IO):
      1) Pre-validate permission name (grammar authority)
      2) Run governance policies (first deny wins)
      3) Evaluate RBAC policy (deny-wins engine)
      4) Default deny if no allow matched
    """
    policy_provider: PolicyProvider
    governance_policies: Tuple[GovernancePolicy, ...] = ()

    # ---------- Public API ----------

    def decide(self, frame: ExecutionFrame, permission: str) -> AccessDecision:
        assert_not_none(frame, "frame")
        assert_not_none(permission, "permission")

        # 1) Validate permission grammar early to prevent accidental drift
        try:
            p = validate_permission_name(permission)
        except GrammarViolationError as e:
            return AccessDecision(
                allowed=False,
                stage=DecisionStage.DEFAULT_DENY,
                reason=f"deny: invalid permission grammar ({e.message})",
                evaluated_roles=tuple(frame.actor.roles),
                permission=permission,
            )

        # 2) Governance policies — first deny wins
        gov_reason = self._evaluate_governance(tenant_id=frame.tenant_id, permission=p)
        if gov_reason is not None:
            return AccessDecision(
                allowed=False,
                stage=DecisionStage.GOVERNANCE,
                reason=f"deny: governance ({gov_reason})",
                evaluated_roles=tuple(frame.actor.roles),
                permission=p,
            )

        # 3) RBAC deny-wins evaluation
        policy = self.policy_provider.policy_for(frame.tenant_id)
        subject = ActorService.to_subject(frame.actor)  # pure subject; no evaluation here
        dec = rbac_evaluate(policy, subject, Permission(p))

        if dec.allowed:
            return AccessDecision(
                allowed=True,
                stage=DecisionStage.RBAC,
                reason=dec.reason,
                role=dec.role,
                pattern=dec.pattern,
                evaluated_roles=tuple(frame.actor.roles),
                permission=p,
            )

        # 4) Default deny (deny-wins, no match)
        return AccessDecision(
            allowed=False,
            stage=DecisionStage.RBAC,
            reason=dec.reason,  # includes "deny: default" from core engine
            role=dec.role,
            pattern=dec.pattern,
            evaluated_roles=tuple(frame.actor.roles),
            permission=p,
        )

    def require(self, frame: ExecutionFrame, permission: str) -> None:
        """
        Raise AuthorizationError on deny (for call-sites that prefer exceptions).
        """
        decision = self.decide(frame, permission)
        if decision.allowed:
            return
        raise AuthorizationError(decision.reason)

    # ---------- Internals ----------

    def _evaluate_governance(self, *, tenant_id, permission: str) -> str | None:
        for gp in self.governance_policies:
            reason = gp.evaluate(tenant_id=tenant_id, permission=permission)
            if reason is not None:
                return reason  # first deny wins
        return None