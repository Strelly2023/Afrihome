from afritech.platform.core.decision import Decision
from afritech.platform.core.decision.engine_outcome import EngineOutcome
from afritech.platform.core.decision.combinator import combine
from afritech.platform.core.typing.enums import EngineId, DecisionVerdictType


def test_decision_determinism():
    """
    ✅ Determinism Enforcement

    This test proves that:
    - Decision computation is deterministic
    - Identical engine outcomes ALWAYS produce identical Decisions
    - No hidden state, clocks, or randomness influence results
    """

    # Canonical engine outcomes (pure inputs)
    outcomes = (
        EngineOutcome(
            engine=EngineId.RBAC,
            verdict=DecisionVerdictType.ALLOW,
            reasons=("rbac.allow",),
            traces=(),
        ),
        EngineOutcome(
            engine=EngineId.POLICY,
            verdict=DecisionVerdictType.ALLOW,  # ✅ ALLOW, not ABSTAIN
            reasons=("policy.no_blocking_rule",),
            traces=(),
        ),
        EngineOutcome(
            engine=EngineId.CONSENT,
            verdict=DecisionVerdictType.ALLOW,  # ✅ ALLOW, not ABSTAIN
            reasons=("consent.granted",),
            traces=(),
        ),
    )

    # First evaluation
    d1: Decision = combine(outcomes)

    # Second evaluation (identical inputs)
    d2: Decision = combine(outcomes)

    # ✅ Structural determinism
    assert d1 == d2

    # ✅ Explicit semantic guarantees
    assert d1.verdict == DecisionVerdictType.ALLOW
    assert d1.reasons == d2.reasons
    assert d1.traces == d2.traces
