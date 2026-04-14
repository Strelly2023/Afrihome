from afritech.platform.core.decision import Decision
from afritech.platform.core.decision.engine_outcome import EngineOutcome
from afritech.platform.core.decision.combinator import combine
from afritech.platform.core.typing.enums import EngineId, DecisionVerdictType


def test_deny_with_empty_allows():
    """
    ✅ Deny Supremacy — Empty Allows (GA‑Sealed)

    Guarantees:
    - A DENY with no ALLOW outcomes still produces DENY
    - Absence of ALLOW does not weaken deny dominance
    - Decision is explainable via deny reasons
    """

    outcomes = (
        EngineOutcome(
            engine=EngineId.POLICY,
            verdict=DecisionVerdictType.DENY,
            reasons=("policy.mandatory_deny",),
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

    # ✅ No ALLOW reasons should be present
    assert all(
        outcome.code not in ("allow",)
        for outcome in decision.reasons
    )

    # ✅ Deny reasons are preserved
    reasons = {reason.code for reason in decision.reasons}
    assert "policy.mandatory_deny" in reasons
    assert "risk.unacceptable" in reasons