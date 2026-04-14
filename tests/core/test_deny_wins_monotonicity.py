from afritech.platform.core.decision import Decision
from afritech.platform.core.decision.engine_outcome import EngineOutcome
from afritech.platform.core.decision.combinator import combine
from afritech.platform.core.typing.enums import EngineId, DecisionVerdictType


def test_deny_wins_monotonicity():
    """
    ✅ Deny‑Wins Monotonicity Enforcement

    This test proves:
    - A single DENY outcome always forces the final Decision to DENY
    - Adding additional ALLOW outcomes can NEVER flip DENY → ALLOW
    """

    # Base case: all engines allow
    base_outcomes = (
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
    )

    decision_allow = combine(base_outcomes)

    assert decision_allow.verdict == DecisionVerdictType.ALLOW

    # Monotonic extension: introduce a single DENY
    extended_outcomes = base_outcomes + (
        EngineOutcome(
            engine=EngineId.CONSENT,
            verdict=DecisionVerdictType.DENY,
            reasons=("consent.revoked",),
            traces=(),
        ),
    )

    decision_deny = combine(extended_outcomes)

    # ✅ Deny‑wins guarantee
    assert decision_deny.verdict == DecisionVerdictType.DENY

    # ✅ Adding more ALLOWs must NOT flip the decision
    further_extended = extended_outcomes + (
        EngineOutcome(
            engine=EngineId.QUOTA,
            verdict=DecisionVerdictType.ALLOW,
            reasons=("quota.available",),
            traces=(),
        ),
    )

    decision_still_deny = combine(further_extended)

    assert decision_still_deny.verdict == DecisionVerdictType.DENY