from __future__ import annotations
# afritech/platform/core/policy/policy_engine.py
"""
GA Enterprise Core — Policy Engine (GA-SEALED)
---------------------------------------------

GA-SEALED

Authorization semantics in this file are frozen.
Any semantic change requires an Architecture Decision Record (ADR).

LAYER: L2 (Pure Engine)
ROLE: Declarative policy evaluation engine

PURPOSE:
- Evaluate policy rules over attributes
- Enforce deny-wins semantics within policy
- Emit semantic outcomes for combination with other engines

CONSTITUTIONAL RULES:
- Pure logic ONLY
- NO IO
- NO time
- NO retries
- NO orchestration
- NO identity, tenancy, or execution context awareness
- MUST be deterministic

PUBLIC API GUARANTEE:
- The symbol `PolicyEngine` MUST remain available for GA stability.
- Functional logic lives in `evaluate_policy`.
"""

from afritech.platform.core.policy.policy_definition import Policy
from afritech.platform.core.decision.engine_outcome import EngineOutcome
from afritech.platform.core.typing.enums import EngineId, DecisionVerdictType
from afritech.platform.core.errors import InvariantViolationError


# ---------------------------------------------------------------------
# Functional Policy Evaluation (Semantic Law)
# ---------------------------------------------------------------------

def evaluate_policy(
    *,
    policy: Policy,
    rbac_allowed: bool,
    attributes: dict[str, object],
) -> EngineOutcome:
    """
    Evaluate a policy against supplied attributes and RBAC precondition.

    SEMANTICS (GA‑LOCKED):

    1. RBAC_FALSE → DENY (policy cannot override RBAC)
    2. Any matching DENY rule → DENY
    3. Any matching ALLOW rule → ALLOW
    4. Otherwise → DENY (secure default; no ABSTAIN in GA model)
    """

    # ----------------------------------------------------
    # Input validation (strict, deterministic)
    # ----------------------------------------------------

    if not isinstance(rbac_allowed, bool):
        raise InvariantViolationError(
            "Policy: rbac_allowed must be a boolean"
        )

    if not isinstance(policy, Policy):
        raise InvariantViolationError(
            "Policy: policy must be a Policy definition"
        )

    if not isinstance(attributes, dict):
        raise InvariantViolationError(
            "Policy: attributes must be a dict"
        )

    # ----------------------------------------------------
    # RBAC prerequisite (fail-fast, authoritative)
    # ----------------------------------------------------

    if not rbac_allowed:
        return EngineOutcome(
            engine=EngineId.POLICY,
            verdict=DecisionVerdictType.DENY,
            reasons=("deny: rbac",),
            traces=(),
        )

    # ----------------------------------------------------
    # PASS 1 — DENY rules (deny-wins)
    # ----------------------------------------------------

    for rule in policy.rules:
        if rule.effect == "deny":
            if all(cond.matches(attributes) for cond in rule.conditions):
                return EngineOutcome(
                    engine=EngineId.POLICY,
                    verdict=DecisionVerdictType.DENY,
                    reasons=("deny: policy",),
                    traces=(),
                )

    # ----------------------------------------------------
    # PASS 2 — ALLOW rules
    # ----------------------------------------------------

    for rule in policy.rules:
        if rule.effect == "allow":
            if all(cond.matches(attributes) for cond in rule.conditions):
                return EngineOutcome(
                    engine=EngineId.POLICY,
                    verdict=DecisionVerdictType.ALLOW,
                    reasons=("allow: policy",),
                    traces=(),
                )

    # ----------------------------------------------------
    # DEFAULT — DENY (GA-aligned, secure fallback)
    # ----------------------------------------------------
    # GA RULE:
    # Policy does NOT abstain.
    # Absence of an allow rule is treated as denial
    # to prevent privilege escalation by omission.

    return EngineOutcome(
        engine=EngineId.POLICY,
        verdict=DecisionVerdictType.DENY,
        reasons=("deny: default",),
        traces=(),
    )


# ---------------------------------------------------------------------
# GA-Stable Object Facade (DO NOT REMOVE)
# ---------------------------------------------------------------------

class PolicyEngine:
    """
    GA-stable object façade for the Policy Engine.

    This class exists to preserve the public API and legacy test usage.
    All semantic logic is delegated to `evaluate_policy`.
    """

    def evaluate(
        self,
        *,
        policy: Policy,
        rbac_allowed: bool,
        attributes: dict[str, object],
    ) -> EngineOutcome:
        return evaluate_policy(
            policy=policy,
            rbac_allowed=rbac_allowed,
            attributes=attributes,
        )


# ---------------------------------------------------------------------
# Public ABI (Explicit & Frozen)
# ---------------------------------------------------------------------

__all__ = [
    "PolicyEngine",
    "evaluate_policy",
]