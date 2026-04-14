from afritech.platform.core.decision import Decision
from afritech.platform.core.decision.engine_outcome import EngineOutcome
from afritech.platform.core.decision.combinator import combine
from afritech.platform.core.typing.enums import EngineId, DecisionVerdictType


def test_deny_with_allow_only():
    """
    ✅ Deny Supremacy — One Deny vs Allow‑Only Others (GA‑Sealed)

    Guarantees:
    - A single explicit DENY dominates when all other engines ALLOW
    - No optimistic or threshold‑based escalation to ALLOW
    - Deny reason is preserved for explainability
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
            verdict=DecisionVerdictType.DENY,  # 👈 the only deny
            reasons=("policy.hard_deny",),
            traces=(),
        ),
    )

    decision: Decision = combine(outcomes)

    # ✅ Deny wins against allow‑only set
    assert decision.verdict == DecisionVerdictType.DENY

    # ✅ Deny explanation is present
    reason_codes = {reason.code for reason in decision.reasons}
    assert "policy.hard_deny" in reason_codes