from afritech.platform.core.decision import Decision
from afritech.platform.core.decision.engine_outcome import EngineOutcome
from afritech.platform.core.decision.combinator import combine
from afritech.platform.core.typing.enums import EngineId, DecisionVerdictType


def test_deny_with_conditional_only():
    """
    ✅ Deny Supremacy — DENY + CONDITIONAL Only (GA‑Sealed)

    Guarantees:
    - DENY dominates CONDITIONAL
    - CONDITIONAL does not downgrade denial
    - Only DENY reasons justify a DENY decision
    """

    outcomes = (
        EngineOutcome(
            engine=EngineId.POLICY,
            verdict=DecisionVerdictType.CONDITIONAL,
            reasons=("policy.pending_additional_requirements",),
            traces=(),
        ),
        EngineOutcome(
            engine=EngineId.RISK,
            verdict=DecisionVerdictType.DENY,  # 👈 decisive deny
            reasons=("risk.unacceptable",),
            traces=(),
        ),
    )

    decision: Decision = combine(outcomes)

    # ✅ DENY dominates CONDITIONAL
    assert decision.verdict == DecisionVerdictType.DENY

    # ✅ Only deny reasons are retained
    reason_codes = {reason.code for reason in decision.reasons}
    assert reason_codes == {"risk.unacceptable"}