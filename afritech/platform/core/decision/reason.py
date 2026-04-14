from __future__ import annotations
# afritech/platform/core/decision/reason.py

"""
Afritech Core — DecisionReason (GA-SEALED)
-----------------------------------------

GA-SEALED

This module defines the immutable, structured justification emitted
by decision engines to explain *why* a particular effect occurred.

Any semantic change requires an Architecture Decision Record (ADR).

LAYER: L1 (Core)
ROLE: Canonical justification atom
"""

from dataclasses import dataclass
from typing import Mapping, Any, Union

from afritech.platform.core.typing.enums import EngineId
from afritech.platform.core.errors import InvariantViolationError


# ---------------------------------------------------------------------
# DecisionReason (Semantic Justification Atom)
# ---------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class DecisionReason:
    """
    Structured justification produced by a decision engine.

    GA CONTRACT:
    - `code` is the canonical semantic identity.
    - Equality and hashing are defined by `code` ONLY.
    - Engine and metadata provide context, not identity.
    """

    engine: Union[EngineId, str]
    code: str
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
                f"DecisionReason.engine must be EngineId or valid string, "
                f"got {self.engine!r}"
            ) from exc

        # Validate code
        if not isinstance(self.code, str) or not self.code:
            raise InvariantViolationError(
                "DecisionReason.code must be a non-empty string"
            )

        # Validate metadata
        if not isinstance(self.metadata, Mapping):
            raise InvariantViolationError(
                "DecisionReason.metadata must be a mapping"
            )

        # Freeze metadata defensively
        object.__setattr__(self, "metadata", dict(self.metadata))

    # -----------------------------------------------------------------
    # ✅ GA‑CRITICAL: Equality & Hashing
    # -----------------------------------------------------------------

    def __eq__(self, other: object) -> bool:
        """
        Equality is defined by semantic code.

        Enables:
        - `"risk_high" in decision.reasons`
        - `set(decision.reasons) == {"risk_high", ...}`
        """
        if isinstance(other, DecisionReason):
            return self.code == other.code
        if isinstance(other, str):
            return self.code == other
        return False

    def __hash__(self) -> int:
        """
        Hash derived solely from the semantic code.
        """
        return hash(self.code)

    # -----------------------------------------------------------------
    # Convenience
    # -----------------------------------------------------------------

    def __str__(self) -> str:
        return self.code


# ---------------------------------------------------------------------
# Public ABI (Explicit & Frozen)
# ---------------------------------------------------------------------

__all__ = ["DecisionReason"]