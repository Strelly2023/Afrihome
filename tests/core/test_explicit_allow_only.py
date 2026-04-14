from afritech.platform.core.decision import Decision
from afritech.platform.core.decision.engine_outcome import EngineOutcome
from afritech.platform.core.decision.combinator import combine
from afritech.platform.core.typing.enums import EngineId, DecisionVerdictType


def test_explicit_allow_only():
    """
    ✅ Explicit Allow Enforcement (GA‑Sealed)

    Guarantees:
    - One or more explicit ALLOW outcomes produce ALLOW
    - No implicit DENY occurs when DENY is absent
    - The decision is explainable via allow reasons
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
    )

    decision: Decision = combine(outcomes)

    # ✅ Explicit allow produces allow
    assert decision.verdict == DecisionVerdictType.ALLOW

    # ✅ Allow reasons are preserved and explainable
    reason_codes = {reason.code for reason in decision.reasons}
    assert "rbac.allow" in reason_codes
    assert "consent.granted" in reason_codes