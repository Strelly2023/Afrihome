from __future__ import annotations

"""
Afritech Core — Decision (GA-SEALED)
-----------------------------------

GA-SEALED

This module defines the canonical, immutable representation of a
decision outcome produced by the Afritech decision system.

Any semantic change requires an Architecture Decision Record (ADR).

LAYER: L2 (Core)
ROLE: Final semantic decision artifact

PURPOSE:
- Provide a normalized decision shape across all engines
- Enable deterministic composition and replay
- Separate decision *meaning* from decision *process*

RULES:
- Pure data ONLY
- NO execution
- NO time
- NO IO
- NO engine logic
- NO orchestration
- MUST be immutable
"""

from dataclasses import dataclass
from typing import Iterable, Tuple, Union

from afritech.platform.core.typing.enums import DecisionVerdictType
from afritech.platform.core.decision.reason import DecisionReason
from afritech.platform.core.decision.trace import DecisionTrace
from afritech.platform.core.errors import InvariantViolationError


# ---------------------------------------------------------------------
# Public semantic verdict (ABI-stable alias)
# ---------------------------------------------------------------------

# NOTE:
# DecisionVerdict is intentionally re-exported here as a module-level
# alias for ABI stability. Semantic authority lives in
# core.typing.enums.DecisionVerdictType.
DecisionVerdict = DecisionVerdictType


# ---------------------------------------------------------------------
# Canonical Decision (Semantic Law)
# ---------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class Decision:
    """
    Canonical decision outcome.

    A Decision represents the final, normalized result of one or more
    decision engine evaluations after deterministic combination.

    It CONTAINS:
    - verdict: final semantic verdict
    - reasons: structured semantic explanations
    - traces: immutable factual evaluation evidence

    It DOES NOT:
    - evaluate rules
    - apply precedence
    - interpret governance
    - trigger side effects

    NOTE (GA-CONTRACT):
    - Decision.reasons is a user-visible, canonical explanation surface.
    - It represents FINAL decision justification, not intermediate engine facts.
    - While engines emit string reason codes internally, Decision.reasons
      is the structured, post-combination explanation form.
    """

    verdict: Union[DecisionVerdict, str]
    reasons: Iterable[DecisionReason]
    traces: Iterable[DecisionTrace]

    # -----------------------------------------------------------------
    # Invariants & Normalization (HARD LAW)
    # -----------------------------------------------------------------

    def __post_init__(self) -> None:
        # Normalize verdict → DecisionVerdict enum
        try:
            object.__setattr__(
                self,
                "verdict",
                DecisionVerdict(self.verdict),
            )
        except Exception as exc:
            raise InvariantViolationError(
                f"Decision.verdict must be DecisionVerdict or valid string, "
                f"got {self.verdict!r}"
            ) from exc

        # Normalize reasons → tuple[DecisionReason]
        try:
            normalized_reasons: Tuple[DecisionReason, ...] = tuple(self.reasons)
        except TypeError as exc:
            raise InvariantViolationError(
                "Decision.reasons must be iterable of DecisionReason"
            ) from exc

        if not all(isinstance(r, DecisionReason) for r in normalized_reasons):
            raise InvariantViolationError(
                "Decision.reasons must contain DecisionReason objects only"
            )

        object.__setattr__(self, "reasons", normalized_reasons)

        # Normalize traces → tuple[DecisionTrace]
        try:
            normalized_traces: Tuple[DecisionTrace, ...] = tuple(self.traces)
        except TypeError as exc:
            raise InvariantViolationError(
                "Decision.traces must be iterable of DecisionTrace"
            ) from exc

        if not all(isinstance(t, DecisionTrace) for t in normalized_traces):
            raise InvariantViolationError(
                "Decision.traces must contain DecisionTrace objects only"
            )

        object.__setattr__(self, "traces", normalized_traces)

    # -----------------------------------------------------------------
    # Derived Views (NON-AUTHORITATIVE)
    # -----------------------------------------------------------------

    @property
    def allowed(self) -> bool:
        """
        Convenience predicate indicating whether the decision permits action.

        NOTE:
        - This is a derived view only
        - It does NOT encode deny-wins or governance logic
        """
        return self.verdict is DecisionVerdict.ALLOW


# ---------------------------------------------------------------------
# Public ABI (Explicit & Frozen)
# ---------------------------------------------------------------------

__all__ = [
    "Decision",
    "DecisionVerdict",
]
