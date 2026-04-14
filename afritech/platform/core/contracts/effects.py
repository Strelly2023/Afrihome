from __future__ import annotations

"""
AfriTech Core Contracts â€” Effects (GA-Sealed)

This module defines the declarative contract for post-decision effects
within the AfriTech platform.

Effects describe *what may happen* after a decision is made.
They do NOT describe *how* or *when* the effect is executed.

PURPOSE:
- Standardize post-decision effect declarations
- Enable deterministic reasoning about outcomes
- Provide a stable contract between decisions and execution layers

RULES:
- Pure data ONLY
- NO execution
- NO IO
- NO time
- NO orchestration
- NO enforcement
- MUST be immutable

Any change requires an ADR.
"""

from dataclasses import dataclass, field
from typing import Mapping, Any
from types import MappingProxyType


# ============================================================================
# Effect Contract (Declarative, Immutable)
# ============================================================================

@dataclass(frozen=True, slots=True)
class EffectContract:
    """
    Declarative description of a post-decision effect.

    An EffectContract defines:
    - the type of effect that may occur
    - an opaque payload describing the effect parameters

    It does NOT:
    - execute the effect
    - schedule the effect
    - enforce ordering
    - interact with infrastructure
    - interpret payload semantics

    Execution is the responsibility of higher layers
    (e.g. control_plane and infrastructure).
    """

    effect_type: str
    payload: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )

    # ------------------------------------------------------------------
    # Post-init normalization (deep immutability guarantee)
    # ------------------------------------------------------------------

    def __post_init__(self) -> None:
        """
        Ensure payload is deeply immutable, even if a mutable
        mapping is provided by the caller.
        """
        object.__setattr__(
            self,
            "payload",
            MappingProxyType(dict(self.payload)),
        )
