import pytest
from dataclasses import FrozenInstanceError

from afritech.platform.core.decision.decision import Decision
from afritech.platform.core.decision.trace import DecisionTrace
from afritech.platform.core.typing.enums import (
    DecisionVerdictType,
    EngineId,
    Effect,
)


def test_decision_trace_immutability():
    """
    ✅ Trace Immutability Enforcement (GA‑Sealed)

    Guarantees:
    - Decision.traces contain DecisionTrace objects only
    - Decision instances are deeply immutable
    - Traces cannot be reassigned or mutated
    """

    trace = DecisionTrace(
        engine=EngineId.RBAC,
        effect=Effect.ALLOW,
        metadata={},
    )

    d1 = Decision(
        verdict=DecisionVerdictType.ALLOW,
        reasons=(),
        traces=(trace,),
    )

    d2 = Decision(
        verdict=DecisionVerdictType.ALLOW,
        reasons=(),
        traces=(trace,),
    )

    # ✅ Content equality
    assert d1.traces == d2.traces

    # ✅ No shared tuple reference
    assert d1.traces is not d2.traces

    # ✅ Reassignment forbidden (dataclass immutability)
    with pytest.raises((TypeError, FrozenInstanceError)):
        d1.traces += (trace,)  # type: ignore

    # ✅ Element mutation forbidden (tuple immutability)
    with pytest.raises(TypeError):
        d1.traces[0] = trace  # type: ignore