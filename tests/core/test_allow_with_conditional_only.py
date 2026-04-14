from afritech.platform.core.decision import Decision
from afritech.platform.core.decision.engine_outcome import EngineOutcome
from afritech.platform.core.decision.combinator import combine
from afritech.platform.core.typing.enums import EngineId, DecisionVerdictType


def test_allow_with_conditional_only():
    """
    ✅ Allow Supremacy — ALLOW + CONDITIONAL Only (GA‑Sealed)

    Guarantees:
    - ALLOW dominates CONDITIONAL
    - CONDITIONAL does not block permission
    - Only ALLOW reasons justify an ALLOW decision
    """

    outcomes = (
        EngineOutcome(
            engine=EngineId.POLICY,
            verdict=DecisionVerdictType.CONDITIONAL,
            reasons=("policy.additional_checks_possible",),
            traces=(),
        ),
        EngineOutcome(
            engine=EngineId.RISK,
            verdict=DecisionVerdictType.CONDITIONAL,
            reasons=("risk.monitoring_recommended",),
            traces=(),
        ),
        EngineOutcome(
            engine=EngineId.RBAC,
            verdict=DecisionVerdictType.ALLOW,  # 👈 decisive allow
            reasons=("rbac.allow",),
            traces=(),
        ),
    )

    decision: Decision = combine(outcomes)

    # ✅ ALLOW dominates CONDITIONAL
    assert decision.verdict == DecisionVerdictType.ALLOW

    # ✅ Only allow reasons are retained
    reason_codes = {reason.code for reason in decision.reasons}
    assert reason_codes == {"rbac.allow"}
