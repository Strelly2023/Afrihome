from __future__ import annotations

"""
GA Enterprise Core â€” Identity Base Models
----------------------------------------

LAYER: L1 (Foundation)
Dependencies: core.typing + core.errors.base + stdlib
Deterministic: YES
Side effects: NONE

Purpose:
- Define canonical identity value structures
- Represent identity ownership within a tenant boundary
- Provide immutable, replay-safe identity models

Rules:
- No authentication logic
- No authorization or RBAC logic
- No persistence assumptions
- No IO, time, or UUID access
- Structural invariants MUST raise ValidationError
"""

from dataclasses import dataclass

from afritech.platform.core.typing import (
    UserId,
    TenantId,
    Version,
    FrozenModel,
)
from afritech.platform.core.errors.base import ValidationError


# ============================================================
# Identity Reference
# ============================================================

@dataclass(frozen=True, slots=True)
class IdentityRef(FrozenModel):
    """
    Stable reference to an identity within a tenant boundary.

    This is a VALUE OBJECT, not a persistence handle.
    """

    user_id: UserId
    tenant_id: TenantId

    def __post_init__(self) -> None:
        if self.user_id is None:
            raise ValidationError(
                "user_id must not be None",
                metadata={"field": "user_id"},
            )

        if self.tenant_id is None:
            raise ValidationError(
                "tenant_id must not be None",
                metadata={"field": "tenant_id"},
            )


# ============================================================
# User Identity Snapshot (GA v1)
# ============================================================

@dataclass(frozen=True, slots=True)
class User(FrozenModel):
    """
    Immutable User identity snapshot (GA v1).

    Notes:
    - Identity == User in GA v1
    - No authentication state included
    - No authorization semantics included
    - Lifecycle is represented by `active` flag only
    """

    id: UserId
    tenant_id: TenantId
    active: bool
    version: Version

    def __post_init__(self) -> None:
        # ----------------------------------------------------
        # Structural validation (fail-fast, deterministic)
        # ----------------------------------------------------

        if self.id is None:
            raise ValidationError(
                "id must not be None",
                metadata={"field": "id"},
            )

        if self.tenant_id is None:
            raise ValidationError(
                "tenant_id must not be None",
                metadata={"field": "tenant_id"},
            )

        if not isinstance(self.active, bool):
            raise ValidationError(
                "active must be a boolean",
                metadata={"active": self.active},
            )

        if not isinstance(self.version, Version):
            raise ValidationError(
                "version must be a Version",
                metadata={"version": self.version},
            )

    # --------------------------------------------------------
    # Deterministic State Transitions
    # --------------------------------------------------------

    def activate(self) -> "User":
        """
        Activate the user identity.

        Returns:
            New User with `active=True`.
        """
        if self.active:
            return self

        return User(
            id=self.id,
            tenant_id=self.tenant_id,
            active=True,
            version=Version(self.version + 1),
        )

    def deactivate(self) -> "User":
        """
        Deactivate the user identity.

        Returns:
            New User with `active=False`.
        """
        if not self.active:
            return self

        return User(
            id=self.id,
            tenant_id=self.tenant_id,
            active=False,
            version=Version(self.version + 1),
        )


# ============================================================
# Identity Snapshot ABI (explicit, frozen)
# ============================================================

__all__ = [
    "IdentityRef",
    "User",
]
