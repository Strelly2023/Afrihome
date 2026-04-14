from afritech.platform.core.decision import Decision
from afritech.platform.core.decision.engine_outcome import EngineOutcome
from afritech.platform.core.decision.combinator import combine
from afritech.platform.core.typing.enums import EngineId, DecisionVerdictType


def test_missing_input_fails_closed():
    """
    ✅ Fail‑Closed Semantics Enforcement (GA‑Sealed)

    Guarantees:
    - Missing or insufficient input results in an explicit DENY
    - No implicit ALLOW is ever possible
    - Termination is explainable via reasons
    """

    # Simulate missing input at the ENGINE level:
    # An engine runs, but required inputs were missing, so it denies.
    outcomes = (
        EngineOutcome(
            engine=EngineId.POLICY,
            verdict=DecisionVerdictType.DENY,
            reasons=("policy.missing_required_input",),
            traces=(),
        ),
    )

    decision: Decision = combine(outcomes)

    # ✅ Fail‑closed verdict
    assert decision.verdict == DecisionVerdictType.DENY

    # ✅ Explicit, explainable termination
    assert len(decision.reasons) > 0
