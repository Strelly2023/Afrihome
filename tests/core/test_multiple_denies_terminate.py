from afritech.platform.core.decision import Decision
from afritech.platform.core.decision.engine_outcome import EngineOutcome
from afritech.platform.core.decision.combinator import combine
from afritech.platform.core.typing.enums import EngineId, DecisionVerdictType


def test_multiple_denies_terminate():
    """
    ✅ Deny Supremacy Enforcement — Multiple Denies (GA‑Sealed)

    Guarantees:
    - Multiple DENY outcomes still produce a DENY decision
    - DENY dominance is idempotent (adding more denies never changes outcome)
    - All deny reasons are preserved for explainability
    """

    outcomes = (
        EngineOutcome(
            engine=EngineId.RBAC,
            verdict=DecisionVerdictType.DENY,
            reasons=("rbac.role_not_permitted",),
            traces=(),
        ),
        EngineOutcome(
            engine=EngineId.POLICY,
            verdict=DecisionVerdictType.DENY,
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
            verdict=DecisionVerdictType.DENY,
            reasons=("risk.too_high",),
            traces=(),
        ),
    )

    decision: Decision = combine(outcomes)

    # ✅ Final verdict must be DENY
    assert decision.verdict == DecisionVerdictType.DENY

    # ✅ All deny reasons must be preserved (order‑independent)
    deny_codes = {reason.code for reason in decision.reasons}

    assert "rbac.role_not_permitted" in deny_codes
    assert "policy.explicit_deny" in deny_codes
    assert "risk.too_high" in deny_codes