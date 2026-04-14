import itertools

from afritech.platform.core.decision import Decision
from afritech.platform.core.decision.engine_outcome import EngineOutcome
from afritech.platform.core.decision.combinator import combine
from afritech.platform.core.typing.enums import EngineId, DecisionVerdictType


def test_engine_order_independence():
    """
    ✅ Engine Order Independence Enforcement

    This test proves:
    - Engine ordering has NO impact on the final Decision
    - combine() is commutative with respect to EngineOutcome order
    """

    outcomes = (
        EngineOutcome(
            engine=EngineId.RBAC,
            verdict=DecisionVerdictType.ALLOW,
            reasons=("rbac.allow",),
            traces=(),
        ),
        EngineOutcome(
            engine=EngineId.POLICY,
            verdict=DecisionVerdictType.ALLOW,
            reasons=("policy.allow",),
            traces=(),
        ),
        EngineOutcome(
            engine=EngineId.CONSENT,
            verdict=DecisionVerdictType.DENY,
            reasons=("consent.revoked",),
            traces=(),
        ),
    )

    # Compute reference decision
    reference_decision = combine(outcomes)

    # Test all permutations of engine orderings
    for permuted_outcomes in itertools.permutations(outcomes):
        decision = combine(permuted_outcomes)

        # ✅ Structural equality required
        assert decision == reference_decision

        # ✅ Explicit semantic guarantee
        assert decision.verdict == DecisionVerdictType.DENY
