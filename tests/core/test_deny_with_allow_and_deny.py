from afritech.platform.core.decision import Decision
from afritech.platform.core.decision.engine_outcome import EngineOutcome
from afritech.platform.core.decision.combinator import combine
from afritech.platform.core.typing.enums import EngineId, DecisionVerdictType


def test_deny_with_allow_and_deny_outcomes():
    """
    ✅ Deny Supremacy — Allow + Deny Present (GA‑Sealed)

    Guarantees:
    - Presence of any DENY dominates any ALLOW outcomes
    - Mixed results never resolve to ALLOW
    - Deny reasons remain visible for explainability
    """

    outcomes = (
        EngineOutcome(
            engine=EngineId.RBAC,
            verdict=DecisionVerdictType.ALLOW,
            reasons=("rbac.allow",),
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
            verdict=DecisionVerdictType.DENY,
            reasons=("risk.too_high",),
            traces=(),
        ),
    )

    decision: Decision = combine(outcomes)

    # ✅ Deny dominates allow
    assert decision.verdict == DecisionVerdictType.DENY

    # ✅ Deny explanation preserved
    reason_codes = {reason.code for reason in decision.reasons}
    assert "risk.too_high" in reason_codes
