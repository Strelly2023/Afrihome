from afritech.platform.core.decision import Decision
from afritech.platform.core.decision.engine_outcome import EngineOutcome
from afritech.platform.core.decision.combinator import combine
from afritech.platform.core.typing.enums import EngineId, DecisionVerdictType


def test_mixed_allow_and_deny():
    """
    ✅ Mixed Allow + Deny Enforcement (GA‑Sealed)

    Guarantees:
    - A single DENY dominates one or more ALLOW outcomes
    - Mixed outcomes never escalate to ALLOW
    - The DENY reason is preserved for explainability
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
            engine=EngineId.POLICY,
            verdict=DecisionVerdictType.DENY,
            reasons=("policy.explicit_deny",),
            traces=(),
        ),
    )

    decision: Decision = combine(outcomes)

    # ✅ Deny supremacy in mixed outcomes
    assert decision.verdict == DecisionVerdictType.DENY

    # ✅ Deny explanation must be present
    reason_codes = {reason.code for reason in decision.reasons}
    assert "policy.explicit_deny" in reason_codes