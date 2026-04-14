from __future__ import annotations

"""
Afritech Core — EngineOutcome (GA-SEALED)
----------------------------------------

GA-SEALED

Authorization semantics in this file are frozen.
Any semantic change requires an Architecture Decision Record (ADR).

LAYER: L1 (Core)
ROLE: Canonical semantic output of a single decision engine

This type represents the semantic contribution of one decision engine
(RBAC, policy, consent, risk, quota, etc.) toward a final decision.

AUTHORITY:
- This object IS semantic truth.
- It MUST be treated as immutable law by all downstream layers.

NOTE (GA-FINAL):
- EngineOutcome is a HARD normalization boundary.
- Legacy inputs (e.g. DecisionReason) are normalized here.
- All downstream layers see only canonical primitives (str).
"""

from dataclasses import dataclass
from typing import (
    Iterable,
    Optional,
    Union,
    FrozenSet,
    TYPE_CHECKING,
)

from afritech.platform.core.typing.enums import EngineId, DecisionVerdictType
from afritech.platform.core.errors import InvariantViolationError

# -------------------------------------------------
# Typing-only import (Pylance/MyPy safe)
# -------------------------------------------------
if TYPE_CHECKING:
    from afritech.platform.core.decision.reason import DecisionReason
else:  # runtime fallback
    DecisionReason = None


# ---------------------------------------------------------------------
# EngineOutcome (Semantic Atom)
# ---------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class EngineOutcome:
    """
    Canonical semantic outcome of a single decision engine.

    ACCEPTS (for construction convenience):
    - engine: EngineId | str
    - verdict: DecisionVerdictType | str
    - reasons: iterable[str | DecisionReason]   (normalized to str)
    - traces: iterable[str]
    - explanation: optional[str]

    STORES (canonically):
    - engine: EngineId
    - verdict: DecisionVerdictType
    - reasons: frozenset[str]
    - traces: frozenset[str]
    - explanation: Optional[str]
    """

    engine: Union[EngineId, str]
    verdict: Union[DecisionVerdictType, str]
    reasons: Iterable[Union[str, "DecisionReason"]]
    traces: Iterable[str] = ()
    explanation: Optional[str] = None

    # -----------------------------------------------------------------
    # Invariants & Normalization (HARD LAW)
    # -----------------------------------------------------------------

    def __post_init__(self) -> None:
        # Normalize engine
        try:
            object.__setattr__(self, "engine", EngineId(self.engine))
        except Exception as exc:
            raise InvariantViolationError(
                f"EngineOutcome.engine must be EngineId or valid string, got {self.engine!r}"
            ) from exc

        # Normalize verdict
        try:
            object.__setattr__(self, "verdict", DecisionVerdictType(self.verdict))
        except Exception as exc:
            raise InvariantViolationError(
                f"EngineOutcome.verdict must be DecisionVerdictType or valid string, "
                f"got {self.verdict!r}"
            ) from exc

        # Normalize reasons → frozenset[str]
        try:
            normalized_reasons: FrozenSet[str] = frozenset(
                r.code if (DecisionReason and isinstance(r, DecisionReason)) else r
                for r in self.reasons
            )
        except TypeError as exc:
            raise InvariantViolationError(
                "EngineOutcome.reasons must be iterable of strings or DecisionReason"
            ) from exc

        if not all(isinstance(r, str) for r in normalized_reasons):
            raise InvariantViolationError(
                "EngineOutcome.reasons must contain strings only"
            )

        object.__setattr__(self, "reasons", normalized_reasons)

        # Normalize traces → frozenset[str]
        try:
            normalized_traces: FrozenSet[str] = frozenset(self.traces)
        except TypeError as exc:
            raise InvariantViolationError(
                "EngineOutcome.traces must be iterable of strings"
            ) from exc

        if not all(isinstance(t, str) for t in normalized_traces):
            raise InvariantViolationError(
                "EngineOutcome.traces must contain strings only"
            )

        object.__setattr__(self, "traces", normalized_traces)

        # Normalize explanation
        if self.explanation is not None and not isinstance(self.explanation, str):
            raise InvariantViolationError(
                "EngineOutcome.explanation must be a string or None"
            )

    # -----------------------------------------------------------------
    # Semantic helpers (READ-ONLY, NON-AUTHORITATIVE)
    # -----------------------------------------------------------------

    @property
    def is_allow(self) -> bool:
        return self.verdict is DecisionVerdictType.ALLOW

    @property
    def is_deny(self) -> bool:
        return self.verdict is DecisionVerdictType.DENY

    @property
    def is_conditional(self) -> bool:
        return self.verdict is DecisionVerdictType.CONDITIONAL

    # -----------------------------------------------------------------
    # Legacy compatibility (GA-SAFE, NON-AUTHORITATIVE)
    # -----------------------------------------------------------------

    @property
    def allowed(self) -> bool:
        return self.verdict is DecisionVerdictType.ALLOW

    @property
    def denied(self) -> bool:
        return self.verdict is DecisionVerdictType.DENY

    @property
    def reason(self) -> str:
        if not self.reasons:
            return ""
        if len(self.reasons) == 1:
            return next(iter(self.reasons))
        return "|".join(sorted(self.reasons))


# ---------------------------------------------------------------------
# Public ABI (Explicit & Frozen)
# ---------------------------------------------------------------------

__all__ = ["EngineOutcome"]