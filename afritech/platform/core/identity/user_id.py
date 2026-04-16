from __future__ import annotations
# afritech/platform/core/identity/user_id.py

"""
GA Enterprise Core — User Identity Identifier
--------------------------------------------

LAYER: Core (Semantic Value Object)

Dependencies:
- stdlib
- core.typing
- core.errors.base

Deterministic: YES
Side effects: NONE
IO / Time / Randomness: NONE

Purpose:
- Define the GA v1 user identity identifier
- Provide a stable, immutable identity value
- Serve as a canonical identity representation in Core

Rules:
- Immutable value object
- No IO
- No randomness
- No time access
- MUST NOT generate identity
- MUST NOT depend on UUID or entropy providers
- Structural invariants MUST raise ValidationError
"""

from dataclasses import dataclass

from afritech.platform.core.typing import (
    UserId as CoreUserId,
)
from afritech.platform.core.errors.base import ValidationError


# ============================================================
# UserId (GA v1)
# ============================================================

@dataclass(frozen=True, slots=True)
class UserId:
    """
    GA v1 User Identity Identifier.

    IMPORTANT:
    - This is a VALUE OBJECT (pure)
    - Identity creation happens OUTSIDE Core (control_plane)
    - This class only wraps and validates identity values
    """

    value: str

    def __post_init__(self) -> None:
        if not isinstance(self.value, str) or not self.value.strip():
            raise ValidationError(
                "UserId must be a non-empty string",
                metadata={"value": self.value},
            )

    def __str__(self) -> str:
        return self.value

    # --------------------------------------------------------
    # Cross-layer compatibility
    # --------------------------------------------------------

    def to_core(self) -> CoreUserId:
        """
        Convert to core.typing.UserId for cross-layer compatibility.
        """
        return CoreUserId(self.value)

    @staticmethod
    def from_core(cid: CoreUserId) -> "UserId":
        """
        Convert from core.typing.UserId.
        """
        return UserId(str(cid))


# ============================================================
# UserId ABI (explicit, frozen)
# ============================================================

__all__ = [
    "UserId",
]