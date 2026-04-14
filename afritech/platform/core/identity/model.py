from __future__ import annotations

"""
GA Enterprise Core â€” Identity Models
-----------------------------------

LAYER: L1 (Foundation)
Dependencies: core.typing + core.errors.base + stdlib
Deterministic: YES
Side effects: NONE

Purpose:
- Define identity-related value models
- Represent principals and identity snapshots
- Remain decoupled from RBAC, policy, and kernel invariants

Rules:
- Pure value objects only
- No kernel dependencies
- Structural invariants MUST raise ValidationError
"""

from dataclasses import dataclass
from typing import NewType, Tuple

from afritech.platform.core.typing import (
    UserId,
    RoleName,
    FrozenModel,
)
from afritech.platform.core.errors.base import ValidationError


# ============================================================
# Identity Identifier
# ============================================================

IdentityId = NewType("IdentityId", str)


# ============================================================
# Principal
# ============================================================

@dataclass(frozen=True, slots=True)
class Principal(FrozenModel):
    """
    External, human-visible representation of an identity.

    Examples:
    - email address
    - username
    - service account name

    Notes:
    - Pure value object
    - No normalization or lookup performed here
    """

    value: str

    def __post_init__(self) -> None:
        if not isinstance(self.value, str) or not self.value.strip():
            raise ValidationError(
                "principal.value must be a non-empty string",
                metadata={"value": self.value},
            )


# ============================================================
# Identity Snapshot (Backward-Compatible View)
# ============================================================

@dataclass(frozen=True, slots=True)
class Identity(FrozenModel):
    """
    Immutable identity snapshot.

    Represents the canonical source of roles
    for downstream authorization engines.

    IMPORTANT:
    - This is a VALUE VIEW, not a persistence model
    - It carries NO authorization logic
    - RBAC consumes this; it does not live here
    """

    user_id: UserId
    roles: Tuple[RoleName, ...] = ()

    def __post_init__(self) -> None:
        # Minimal structural invariant only
        if self.user_id is None:
            raise ValidationError(
                "identity.user_id must not be None",
                metadata={"field": "user_id"},
            )
