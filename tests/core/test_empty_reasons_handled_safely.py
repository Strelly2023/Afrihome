from afritech.platform.core.decision import Decision
from afritech.platform.core.decision.engine_outcome import EngineOutcome
from afritech.platform.core.decision.combinator import combine
from afritech.platform.core.typing.enums import EngineId, DecisionVerdictType


def test_empty_engine_reasons_are_preserved():
    """
    ✅ Explanation Boundary Enforcement (GA‑Sealed)

    Guarantees:
    - EngineOutcome may be silent
    - Decision may be silent
    - No synthetic reasons are invented by the core
    """

    outcome = EngineOutcome(
        engine=EngineId.POLICY,
        verdict=DecisionVerdictType.DENY,
        reasons=(),  # ✅ allowed
        traces=(),
    )

    decision: Decision = combine((outcome,))

    # ✅ Verdict is correct
    assert decision.verdict == DecisionVerdictType.DENY

    # ✅ Silence is preserved (no synthetic explanation)
    assert decision.reasons == ()