from __future__ import annotations

"""
Afritech Core — Decision Combinator (GA-SEALED)
----------------------------------------------

GA-SEALED

Authorization semantics in this file are frozen.
Any semantic change requires an Architecture Decision Record (ADR).

LAYER: L2 (Core)
ROLE: Final semantic authority for authorization decisions

PURPOSE:
- Enforce platform-wide authorization semantics
- Preserve deny-wins precedence
- Combine independent engine truths
- Enable replay-safe, auditable decisions

CONSTITUTIONAL RULES:
- Pure logic ONLY
- NO IO
- NO time
- NO retries
- NO orchestration
- NO engine-specific semantics
- MUST be deterministic
"""

from typing import Iterable, Set

from afritech.platform.core.decision.engine_outcome import EngineOutcome
from afritech.platform.core.decision.decision import Decision
from afritech.platform.core.decision.reason import DecisionReason
from afritech.platform.core.typing.enums import (
    EngineId,
    DecisionVerdictType,
)
from afritech.platform.core.errors import InvariantViolationError


# ---------------------------------------------------------------------
# Deterministic Decision Combinator (GA Law)
# ---------------------------------------------------------------------

def combine(outcomes: Iterable[EngineOutcome]) -> Decision:
    """
    Deterministically combine multiple EngineOutcome objects into
    a single canonical Decision.

    CONSTITUTIONAL DECISION RULES (GA-SEALED):

    1. If ANY EngineOutcome has verdict DENY → final verdict is DENY
    2. Else, if ANY EngineOutcome has verdict ALLOW → final verdict is ALLOW
    3. Else, if ANY EngineOutcome has verdict CONDITIONAL → final verdict is CONDITIONAL
    4. Otherwise → DENY (defensive fallback)

    PROPERTIES:
    - Order-independent
    - Deterministic
    - Engine-agnostic
    - Replay-safe

    PUBLIC ABI RULE:
    - Decision.reasons is a tuple[DecisionReason]
    """

    outcomes = tuple(outcomes)

    if not outcomes:
        raise InvariantViolationError(
            "Decision combinator requires at least one EngineOutcome"
        )

    deny_reasons: Set[str] = set()
    allow_reasons: Set[str] = set()
    conditional_reasons: Set[str] = set()
    all_traces: Set[str] = set()

    # -----------------------------------------------------------------
    # Aggregate engine outcomes (order-independent)
    # -----------------------------------------------------------------

    for outcome in outcomes:
        if not isinstance(outcome, EngineOutcome):
            raise InvariantViolationError(
                f"Invalid input to decision combinator: {outcome!r}"
            )

        all_traces.update(outcome.traces)

        if outcome.verdict is DecisionVerdictType.DENY:
            deny_reasons.update(outcome.reasons)

        elif outcome.verdict is DecisionVerdictType.ALLOW:
            allow_reasons.update(outcome.reasons)

        elif outcome.verdict is DecisionVerdictType.CONDITIONAL:
            conditional_reasons.update(outcome.reasons)

        else:
            raise InvariantViolationError(
                f"Unsupported verdict in EngineOutcome: {outcome.verdict!r}"
            )

    # -----------------------------------------------------------------
    # Verdict resolution (constitutional precedence)
    # -----------------------------------------------------------------

    if deny_reasons:
        return Decision(
            verdict=DecisionVerdictType.DENY,
            reasons=tuple(
                DecisionReason(
                    engine=EngineId.COMBINED,
                    code=code,
                    metadata={},
                )
                for code in sorted(deny_reasons)
            ),
            traces=tuple(sorted(all_traces)),
        )

    if allow_reasons:
        return Decision(
            verdict=DecisionVerdictType.ALLOW,
            reasons=tuple(
                DecisionReason(
                    engine=EngineId.COMBINED,
                    code=code,
                    metadata={},
                )
                for code in sorted(allow_reasons)
            ),
            traces=tuple(sorted(all_traces)),
        )

    if conditional_reasons:
        return Decision(
            verdict=DecisionVerdictType.CONDITIONAL,
            reasons=tuple(
                DecisionReason(
                    engine=EngineId.COMBINED,
                    code=code,
                    metadata={},
                )
                for code in sorted(conditional_reasons)
            ),
            traces=tuple(sorted(all_traces)),
        )

    # -----------------------------------------------------------------
    # Defensive fallback (should be unreachable)
    # -----------------------------------------------------------------

    return Decision(
        verdict=DecisionVerdictType.DENY,
        reasons=(),
        traces=tuple(sorted(all_traces)),
    )


# ---------------------------------------------------------------------
# Public ABI (Explicit & Frozen)
# ---------------------------------------------------------------------

__all__ = ["combine"]