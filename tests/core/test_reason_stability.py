from afritech.platform.core.decision import Decision
from afritech.platform.core.decision.engine_outcome import EngineOutcome
from afritech.platform.core.decision.combinator import combine
from afritech.platform.core.decision.reason import DecisionReason
from afritech.platform.core.typing.enums import EngineId, DecisionVerdictType


def test_decision_reason_stability():
    """
    ✅ Reason Stability Enforcement (GA‑Sealed)

    Guarantees:
    - Reasons are deterministic
    - Reasons are structured (DecisionReason)
    - Reason content is stable (order-independent)
    - Identical inputs → identical reasons
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
    )

    d1: Decision = combine(outcomes)
    d2: Decision = combine(outcomes)

    # ✅ Structural determinism
    assert d1.reasons == d2.reasons

    # ✅ Structured reasons
    assert all(isinstance(r, DecisionReason) for r in d1.reasons)

    # ✅ Content stability (order-independent)
    assert {r.code for r in d1.reasons} == {
        "rbac.allow",
        "policy.allow",
    }

    assert {r.code for r in d2.reasons} == {
        "rbac.allow",
        "policy.allow",
    }