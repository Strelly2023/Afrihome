from afritech.platform.core.decision import Decision
from afritech.platform.core.decision.engine_outcome import EngineOutcome
from afritech.platform.core.decision.combinator import combine
from afritech.platform.core.typing.enums import EngineId, DecisionVerdictType


def test_conditional_without_allow_results_in_conditional():
    """
    ✅ Conditional Semantics Enforcement (GA‑Sealed)

    Guarantees:
    - CONDITIONAL does not imply ALLOW
    - In absence of an explicit DENY or ALLOW, CONDITIONAL is preserved
    - Decision remains explicitly undecided (CONDITIONAL)
    """

    outcomes = (
        EngineOutcome(
            engine=EngineId.POLICY,
            verdict=DecisionVerdictType.CONDITIONAL,
            reasons=("policy.condition_not_met",),
            traces=(),
        ),
        EngineOutcome(
            engine=EngineId.RISK,
            verdict=DecisionVerdictType.CONDITIONAL,
            reasons=("risk.review_required",),
            traces=(),
        ),
    )

    decision: Decision = combine(outcomes)

    # ✅ CONDITIONAL is preserved (not escalated, not denied)
    assert decision.verdict == DecisionVerdictType.CONDITIONAL

    # ✅ Conditional reasons are preserved for explainability
    reason_codes = {reason.code for reason in decision.reasons}
    assert "policy.condition_not_met" in reason_codes
    assert "risk.review_required" in reason_codes
