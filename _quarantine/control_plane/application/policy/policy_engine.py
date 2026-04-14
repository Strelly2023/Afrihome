from dataclasses import dataclass
from typing import Mapping, Protocol, Optional
from core.kernel.invariants import assert_not_none
from control_plane.application.authorization.service import AuthorizationService
from control_plane.application.authorization.models import AccessDecision, DecisionStage
from .policy_rule import PolicyRule

# ------- Protocols (pure) --------
class FeatureGate(Protocol):
    def enabled(self, frame, key: str) -> bool: ...

class EntitlementGate(Protocol):
    def has(self, frame, key: str) -> bool: ...

class ABACEvaluator(Protocol):
    def evaluate(self, *, subject: Mapping[str, str], resource: Mapping[str, str], action: str) -> bool: ...

# ------- Engine (orchestration-only) --------
@dataclass(frozen=True, slots=True)
class PolicyEngine:
    """
    Final access composer:
      - RBAC (deny-wins) via AuthorizationService
      - Feature flags (FeatureGate)
      - Entitlements (EntitlementGate)
      - Optional ABAC evaluation
    No IO; purely orchestrates contracts to a final AccessDecision.
    """
    authz: AuthorizationService
    flags: Optional[FeatureGate] = None
    ents: Optional[EntitlementGate] = None
    abac: Optional[ABACEvaluator] = None

    def decide(
        self,
        frame,
        *,
        rule: PolicyRule,
        abac_subject: Mapping[str, str] | None = None,
        abac_resource: Mapping[str, str] | None = None,
    ) -> AccessDecision:
        assert_not_none(frame, "frame")
        assert_not_none(rule, "rule")

        # 1) RBAC (deny-wins)
        d = self.authz.decide(frame, rule.permission)
        if not d.allowed:
            return d

        # 2) Feature gate (optional)
        if self.flags and rule.feature_key and not self.flags.enabled(frame, rule.feature_key):
            return AccessDecision(
                allowed=False, stage=DecisionStage.GOVERNANCE,
                reason=f"deny: feature '{rule.feature_key}' disabled",
                evaluated_roles=d.evaluated_roles, permission=d.permission,
            )

        # 3) Entitlement gate (optional)
        if self.ents and rule.entitlement_key and not self.ents.has(frame, rule.entitlement_key):
            return AccessDecision(
                allowed=False, stage=DecisionStage.GOVERNANCE,
                reason=f"deny: entitlement '{rule.entitlement_key}' missing",
                evaluated_roles=d.evaluated_roles, permission=d.permission,
            )

        # 4) ABAC (optional)
        if self.abac:
            s = abac_subject or {}
            r = abac_resource or {}
            if not self.abac.evaluate(subject=s, resource=r, action=rule.permission):
                return AccessDecision(
                    allowed=False, stage=DecisionStage.GOVERNANCE,
                    reason="deny: ABAC",
                    evaluated_roles=d.evaluated_roles, permission=d.permission,
                )

        # Success: RBAC allowed and every gate passed
        return d