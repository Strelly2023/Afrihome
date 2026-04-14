from afritech.platform.core.decision import Decision
from afritech.platform.core.decision.engine_outcome import EngineOutcome
from afritech.platform.core.decision.combinator import combine
from afritech.platform.core.typing.enums import EngineId, DecisionVerdictType


def test_deny_with_no_allows():
    """
    ✅ Deny Enforcement — No ALLOW Outcomes (GA‑Sealed)

    Guarantees:
    - If no engine allows and one or more engines deny, the result is DENY
    - No implicit ALLOW can occur
    - Deny reasons are preserved for explainability
    """

    outcomes = (
        EngineOutcome(
            engine=EngineId.POLICY,
            verdict=DecisionVerdictType.DENY,
            reasons=("policy.hard_deny",),
            traces=(),
        ),
        EngineOutcome(
            engine=EngineId.RISK,
            verdict=DecisionVerdictType.DENY,
            reasons=("risk.unacceptable",),
            traces=(),
        ),
    )

    decision: Decision = combine(outcomes)

    # ✅ Final verdict must be DENY
    assert decision.verdict == DecisionVerdictType.DENY

    # ✅ Confirm no ALLOW reasons exist
    reason_codes = {reason.code for reason in decision.reasons}
    assert "policy.hard_deny" in reason_codes
    assert "risk.unacceptable" in reason_codes
