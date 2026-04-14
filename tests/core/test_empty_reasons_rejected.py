from afritech.platform.core.decision.combinator import combine
from afritech.platform.core.decision.engine_outcome import EngineOutcome
from afritech.platform.core.typing.enums import DecisionVerdictType, EngineId


def test_empty_engine_reasons_are_preserved():
    """
    ✅ Explanation Boundary Enforcement (GA‑Sealed)

    Guarantees:
    - EngineOutcome may be silent
    - Decision may be silent
    - The core does not invent explanations
    """

    outcome = EngineOutcome(
        engine=EngineId.POLICY,
        verdict=DecisionVerdictType.DENY,
        reasons=(),   # ✅ allowed
        traces=(),
    )

    decision = combine((outcome,))

    assert decision.verdict == DecisionVerdictType.DENY
    assert decision.reasons == ()