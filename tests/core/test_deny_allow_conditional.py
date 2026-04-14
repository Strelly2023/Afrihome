from afritech.platform.core.decision import Decision
from afritech.platform.core.decision.engine_outcome import EngineOutcome
from afritech.platform.core.decision.combinator import combine
from afritech.platform.core.typing.enums import EngineId, DecisionVerdictType


def test_deny_with_allow_and_conditional():
    """
    ✅ Deny Supremacy — DENY + ALLOW + CONDITIONAL (GA‑Sealed)

    Guarantees:
    - DENY dominates ALLOW and CONDITIONAL
    - Mixed outcomes always resolve to DENY
    - Only DENY reasons justify a DENY decision
    """

    outcomes = (
        EngineOutcome(
            engine=EngineId.RBAC,
            verdict=DecisionVerdictType.ALLOW,
            reasons=("rbac.allow",),
            traces=(),
        ),
        EngineOutcome(
            engine=EngineId.POLICY,
            verdict=DecisionVerdictType.CONDITIONAL,
            reasons=("policy.requires_review",),
            traces=(),
        ),
        EngineOutcome(
            engine=EngineId.RISK,
            verdict=DecisionVerdictType.DENY,  # 👈 absolute deny
            reasons=("risk.too_high",),
            traces=(),
        ),
    )

    decision: Decision = combine(outcomes)

    # ✅ Absolute deny supremacy
    assert decision.verdict == DecisionVerdictType.DENY

    # ✅ Only deny reasons are retained
    reason_codes = {reason.code for reason in decision.reasons}
    assert reason_codes == {"risk.too_high"}
