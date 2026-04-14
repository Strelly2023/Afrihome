from afritech.platform.core.decision import Decision
from afritech.platform.core.decision.engine_outcome import EngineOutcome
from afritech.platform.core.decision.combinator import combine
from afritech.platform.core.typing.enums import EngineId, DecisionVerdictType


def test_decisions_must_be_explainable():
    """
    ✅ Explanation Enforcement (GA‑Sealed)

    Guarantees:
    - Every decision outcome is accompanied by at least one reason
    - No ALLOW, DENY, or CONDITIONAL decision is reason‑less
    - Decisions are always audit‑ and human‑explainable
    """

    test_cases = [
        # ✅ Explicit ALLOW
        (
            EngineOutcome(
                engine=EngineId.RBAC,
                verdict=DecisionVerdictType.ALLOW,
                reasons=("rbac.allow",),
                traces=(),
            ),
            DecisionVerdictType.ALLOW,
        ),
        # ✅ Explicit DENY
        (
            EngineOutcome(
                engine=EngineId.POLICY,
                verdict=DecisionVerdictType.DENY,
                reasons=("policy.explicit_deny",),
                traces=(),
            ),
            DecisionVerdictType.DENY,
        ),
        # ✅ CONDITIONAL
        (
            EngineOutcome(
                engine=EngineId.RISK,
                verdict=DecisionVerdictType.CONDITIONAL,
                reasons=("risk.review_required",),
                traces=(),
            ),
            DecisionVerdictType.CONDITIONAL,
        ),
    ]

    for outcome, expected_verdict in test_cases:
        decision: Decision = combine((outcome,))

        # ✅ Correct verdict
        assert decision.verdict == expected_verdict

        # ✅ Decision must be explainable
        assert len(decision.reasons) > 0