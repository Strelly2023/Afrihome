from afritech.platform.core.decision import Decision
from afritech.platform.core.decision.engine_outcome import EngineOutcome
from afritech.platform.core.decision.combinator import combine
from afritech.platform.core.typing.enums import EngineId, DecisionVerdictType


def test_any_domain_deny_terminates():
    """
    ✅ Deny Supremacy Enforcement (GA‑Sealed)

    Guarantees:
    - Any single DENY from any engine dominates
    - No combination of ALLOWs can override a DENY
    - Termination is explicit and explainable via reasons
    """

    outcomes = (
        EngineOutcome(
            engine=EngineId.RBAC,  # identity + capability live here
            verdict=DecisionVerdictType.ALLOW,
            reasons=("rbac.allow",),
            traces=(),
        ),
        EngineOutcome(
            engine=EngineId.POLICY,
            verdict=DecisionVerdictType.DENY,   # 👈 single deny
            reasons=("policy.explicit_deny",),
            traces=(),
        ),
        EngineOutcome(
            engine=EngineId.CONSENT,
            verdict=DecisionVerdictType.ALLOW,
            reasons=("consent.granted",),
            traces=(),
        ),
        EngineOutcome(
            engine=EngineId.RISK,
            verdict=DecisionVerdictType.ALLOW,
            reasons=("risk.acceptable",),
            traces=(),
        ),
    )

    decision: Decision = combine(outcomes)

    # ✅ Deny supremacy
    assert decision.verdict == DecisionVerdictType.DENY

    # ✅ Explicit explanation (no hidden termination field)
    assert any(
        reason.code == "policy.explicit_deny"
        for reason in decision.reasons
    )