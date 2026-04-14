from __future__ import annotations

"""
Afritech Core — DecisionTrace (GA-SEALED)
----------------------------------------

GA-SEALED

This module defines the immutable trace structure used to record
*what each decision engine evaluated* and *what effect it produced*.

Any semantic change requires an Architecture Decision Record (ADR).

LAYER: L1 (Core)
ROLE: Canonical evaluation evidence atom

PURPOSE:
- Provide deterministic, replay-safe evidence
- Enable forensic audit and explanation
- Preserve engine-level effects without interpretation

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
from typing import Mapping, Any, Union, FrozenSet

from afritech.platform.core.typing.enums import EngineId, Effect
from afritech.platform.core.errors import InvariantViolationError


# ---------------------------------------------------------------------
# Canonical Decision Trace (Evidence Atom)
# ---------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class DecisionTrace:
    """
    Immutable trace emitted by a single decision engine evaluation.

    This trace records:
    - which engine evaluated
    - what effect it produced
    - structured metadata describing factual context

    It does NOT:
    - explain precedence
    - justify final outcomes
    - interpret governance or policy
    """

    engine: Union[EngineId, str]
    effect: Union[Effect, str]
    metadata: Mapping[str, Any]

    # -----------------------------------------------------------------
    # Invariants & Normalization (HARD LAW)
    # -----------------------------------------------------------------

    def __post_init__(self) -> None:
        # Normalize engine → EngineId
        try:
            object.__setattr__(self, "engine", EngineId(self.engine))
        except Exception as exc:
            raise InvariantViolationError(
                f"DecisionTrace.engine must be EngineId or valid string, "
                f"got {self.engine!r}"
            ) from exc

        # Normalize effect → Effect
        try:
            object.__setattr__(self, "effect", Effect(self.effect))
        except Exception as exc:
            raise InvariantViolationError(
                f"DecisionTrace.effect must be Effect or valid string, "
                f"got {self.effect!r}"
            ) from exc

        # Normalize metadata → immutable mapping
        if not isinstance(self.metadata, Mapping):
            raise InvariantViolationError(
                "DecisionTrace.metadata must be a mapping"
            )

        try:
            frozen_items: FrozenSet[tuple[str, Any]] = frozenset(self.metadata.items())
        except TypeError as exc:
            raise InvariantViolationError(
                "DecisionTrace.metadata must contain hashable keys"
            ) from exc

        object.__setattr__(self, "metadata", dict(frozen_items))

    # -----------------------------------------------------------------
    # Semantic identity
    # -----------------------------------------------------------------

    def identity(self) -> tuple[EngineId, Effect]:
        """
        Stable semantic identity of this trace.

        Used for deterministic grouping and replay verification.
        """
        return (self.engine, self.effect)


# ---------------------------------------------------------------------
# Public ABI (Explicit & Frozen)
# ---------------------------------------------------------------------

__all__ = [
    "DecisionTrace",
]