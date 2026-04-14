from __future__ import annotations

"""
GA Enterprise Core â€” User Identity Identifier
--------------------------------------------

LAYER: L1 (Foundation)
Dependencies: stdlib + core.typing + core.identity.uuid + core.errors.base
Deterministic: YES
Side effects: NONE

Purpose:
- Define the GA v1 user identity identifier
- Provide a stable, immutable identity value
- Ensure deterministic creation via injected UUID provider

Rules:
- Immutable value object
- No IO
- No randomness
- No time access
- UUIDs must be injected explicitly
- Structural invariants MUST raise ValidationError
"""

from dataclasses import dataclass

from afritech.platform.core.identity.uuid import UUIDProvider
from afritech.platform.core.typing import (
    UserId as CoreUserId,
    AggregateId,
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
    - In GA v1, UserId is the canonical identity identifier
    - Used across authentication, authorization, audit, and RBAC
    - Service/System identities are introduced in GA v2

    This is a VALUE OBJECT, not a persistence handle.
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

    # --------------------------------------------------------
    # GA-canonical deterministic factory
    # --------------------------------------------------------

    @staticmethod
    def new(*, uuid_provider: UUIDProvider) -> "UserId":
        """
        Deterministic factory for creating a new UserId.

        UUID uniqueness MUST be supplied explicitly by the provider
        via a fixed discriminator.
        """
        agg: AggregateId = uuid_provider.aggregate_id(
            discriminator="identity:user"
        )
        return UserId(str(agg))


# ============================================================
# UserId ABI (explicit, frozen)
# ============================================================

__all__ = [
    "UserId",
]
