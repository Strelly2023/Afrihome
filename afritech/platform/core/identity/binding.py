from __future__ import annotations

"""
GA Enterprise Core â€” Identity Binding
------------------------------------

LAYER: L1 (Foundation)
Dependencies: core.identity + core.typing + core.errors.base + stdlib
Deterministic: YES
Side effects: NONE

Purpose:
- Define the canonical binding between an identity and RBAC roles
- Act as the SINGLE authoritative source of roles for authorization engines

Rules:
- Immutable
- No IO
- No time access
- No kernel dependencies
- Structural invariants MUST raise ValidationError
"""

from dataclasses import dataclass
from typing import Optional, Tuple

from afritech.platform.core.identity.model import IdentityId, Principal
from afritech.platform.core.typing import (
    RoleName,
    FrozenModel,
)
from afritech.platform.core.errors.base import ValidationError


# ============================================================
# Identity Binding (Authoritative RBAC Source)
# ============================================================

@dataclass(frozen=True, slots=True)
class IdentityBinding(FrozenModel):
    """
    Canonical binding between an identity and its RBAC roles.

    IMPORTANT:
    - This is the SINGLE formal source of roles for authorization
    - RBAC engines consume this structure; they do not modify it
    - This is a VALUE OBJECT, not a persistence record
    """

    identity_id: IdentityId
    roles: Tuple[RoleName, ...]
    principal: Optional[Principal] = None

    def __post_init__(self) -> None:
        # ----------------------------------------------------
        # Structural validation (fail-fast, deterministic)
        # ----------------------------------------------------

        if self.identity_id is None:
            raise ValidationError(
                "identity_id must not be None",
                metadata={"field": "identity_id"},
            )

        if not isinstance(self.roles, tuple):
            raise ValidationError(
                "roles must be a tuple",
                metadata={"roles_type": type(self.roles).__name__},
            )

        if any(role is None for role in self.roles):
            raise ValidationError(
                "roles must not contain None",
                metadata={"roles": self.roles},
            )

        if self.principal is not None and not isinstance(self.principal, Principal):
            raise ValidationError(
                "principal must be a Principal or None",
                metadata={"principal_type": type(self.principal).__name__},
            )


# ============================================================
# Identity Binding ABI (explicit, frozen)
# ============================================================

__all__ = [
    "IdentityBinding",
]
