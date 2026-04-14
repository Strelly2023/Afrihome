import pytest
from dataclasses import FrozenInstanceError

from afritech.platform.core.decision.decision import Decision
from afritech.platform.core.decision.trace import DecisionTrace
from afritech.platform.core.typing.enums import (
    DecisionVerdictType,
    EngineId,
    Effect,
)


def test_decision_deep_immutability():
    """
    ✅ Deep Immutability Enforcement (GA‑Sealed)

    Guarantees:
    - Decision is a frozen dataclass
    - Containers (reasons, traces) are immutable
    - DecisionTrace identity is immutable
    - Metadata is replace‑protected (but content‑mutable)
    """

    trace = DecisionTrace(
        engine=EngineId.RBAC,
        effect=Effect.ALLOW,
        metadata={"rule": "rbac.allow"},
    )

    decision = Decision(
        verdict=DecisionVerdictType.ALLOW,
        reasons=(),
        traces=(trace,),
    )

    # ------------------------------------------------------------------
    # 1. Top‑level field immutability
    # ------------------------------------------------------------------

    with pytest.raises(FrozenInstanceError):
        decision.verdict = DecisionVerdictType.DENY  # type: ignore

    with pytest.raises(FrozenInstanceError):
        decision.traces = ()  # type: ignore

    # ------------------------------------------------------------------
    # 2. Container immutability
    # ------------------------------------------------------------------

    with pytest.raises((TypeError, FrozenInstanceError)):
        decision.traces += (trace,)  # type: ignore

    with pytest.raises(TypeError):
        decision.traces[0] = trace  # type: ignore

    # ------------------------------------------------------------------
    # 3. Trace identity immutability (NOT deep metadata freeze)
    # ------------------------------------------------------------------

    with pytest.raises(FrozenInstanceError):
        decision.traces[0].engine = EngineId.POLICY  # type: ignore

    with pytest.raises(FrozenInstanceError):
        decision.traces[0].effect = Effect.DENY  # type: ignore

    with pytest.raises(FrozenInstanceError):
        decision.traces[0].metadata = {}  # type: ignore

    # ✅ Metadata CONTENT may mutate (explicitly allowed)
    decision.traces[0].metadata["enriched_by"] = "audit_sink"
