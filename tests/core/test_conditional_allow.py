from afritech.platform.core.decision import Decision
from afritech.platform.core.decision.engine_outcome import EngineOutcome
from afritech.platform.core.decision.combinator import combine
from afritech.platform.core.typing.enums import EngineId, DecisionVerdictType


def test_conditional_with_allow_results_in_allow():
    """
    ✅ Conditional Allow Enforcement (GA‑Sealed)

    Guarantees:
    - CONDITIONAL does not block an explicit ALLOW
    - Explicit ALLOW resolves the decision to ALLOW
    - Only ALLOW reasons are preserved in an ALLOW decision
    """

    outcomes = (
        EngineOutcome(
            engine=EngineId.POLICY,
            verdict=DecisionVerdictType.CONDITIONAL,
            reasons=("policy.requires_additional_check",),
            traces=(),
        ),
        EngineOutcome(
            engine=EngineId.RISK,
            verdict=DecisionVerdictType.CONDITIONAL,
            reasons=("risk.manual_review_suggested",),
            traces=(),
        ),
        EngineOutcome(
            engine=EngineId.RBAC,
            verdict=DecisionVerdictType.ALLOW,
            reasons=("rbac.allow",),
            traces=(),
        ),
    )

    decision: Decision = combine(outcomes)

    # ✅ Explicit ALLOW resolves the decision
    assert decision.verdict == DecisionVerdictType.ALLOW

    # ✅ ONLY allow reasons are retained
    reason_codes = {reason.code for reason in decision.reasons}
    assert reason_codes == {"rbac.allow"}