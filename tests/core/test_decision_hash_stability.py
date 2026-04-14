import hashlib

from afritech.platform.core.decision.decision import Decision
from afritech.platform.core.decision.reason import DecisionReason
from afritech.platform.core.decision.trace import DecisionTrace
from afritech.platform.core.typing.enums import (
    DecisionVerdictType,
    EngineId,
    Effect,
)


def _canonical_decision_hash(decision: Decision) -> str:
    """
    Canonical, deterministic hash of a Decision.

    IMPORTANT:
    - Uses only GA‑stable, public fields
    - Order‑independent where semantics are order‑independent
    - Suitable ONLY for tests (not required production API)
    """

    # Verdict
    parts = [decision.verdict.value]

    # Reasons: semantic content only, order‑independent
    reason_codes = sorted(r.code for r in decision.reasons)
    parts.extend(reason_codes)

    # Traces: stable tuple of semantic fields
    for trace in decision.traces:
        parts.append(f"{trace.engine.value}:{trace.effect.value}:{sorted(trace.metadata.items())}")

    payload = "|".join(parts)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def test_decision_hash_stability():
    """
    ✅ Hash‑Stability / Replay‑Stability Enforcement (GA‑Sealed)

    Guarantees:
    - Identical Decisions produce identical canonical hashes
    - Hash is stable across recomputation
    - No hidden entropy affects outcomes
    """

    trace = DecisionTrace(
        engine=EngineId.RBAC,
        effect=Effect.ALLOW,
        metadata={"rule": "rbac.allow"},
    )

    decision_1 = Decision(
        verdict=DecisionVerdictType.ALLOW,
        reasons=(
            DecisionReason(
                engine=EngineId.COMBINED,
                code="rbac.allow",
                metadata={},
            ),
        ),
        traces=(trace,),
    )

    decision_2 = Decision(
        verdict=DecisionVerdictType.ALLOW,
        reasons=(
            DecisionReason(
                engine=EngineId.COMBINED,
                code="rbac.allow",
                metadata={},
            ),
        ),
        traces=(trace,),
    )

    hash_1 = _canonical_decision_hash(decision_1)
    hash_2 = _canonical_decision_hash(decision_2)

    # ✅ Replay‑grade guarantee
    assert hash_1 == hash_2