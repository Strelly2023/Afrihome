from afritech.platform.core.decision.combinator import combine
from afritech.platform.core.decision.engine_outcome import EngineOutcome
from afritech.platform.core.typing.enums import DecisionVerdictType, EngineId


def test_policy_allow_is_respected_at_core_level():
    """
    ✅ Core Semantics (GA‑Sealed)

    Guarantees:
    - The decision core does not enforce authority isolation
    - Any engine emitting ALLOW may yield ALLOW
    """

    outcomes = (
        EngineOutcome(
            engine=EngineId.POLICY,
            verdict=DecisionVerdictType.ALLOW,
            reasons=("policy.rule_allows_action",),
            traces=(),
        ),
    )

    decision = combine(outcomes)

    assert decision.verdict == DecisionVerdictType.ALLOW
