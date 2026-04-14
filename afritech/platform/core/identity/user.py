from __future__ import annotations

"""
GA Enterprise Core â€” User Identity Aggregate (GA v1)
---------------------------------------------------

LAYER: L2 (Domain Aggregate)
Dependencies: core.identity + core.typing + core.errors.base + stdlib
Deterministic: YES
Side effects: NONE
IO / ORM / Frameworks: NONE

Purpose:
- Represent the GA v1 User identity aggregate
- Own identity lifecycle and descriptive attributes
- Remain reusable by RBAC, audit, and policy layers

IMPORTANT GA v1 RULES:
- Identity == User
- This aggregate does NOT make authorization decisions
- RBAC and Policy engines consume this state; they do not live here
"""

from dataclasses import dataclass, replace
from typing import Tuple

from afritech.platform.core.typing import (
    UnixMillis,
    TenantId,
    RoleName,
    FrozenModel,
)
from afritech.platform.core.errors.base import (
    ValidationError,
    InvariantViolationError,
)

from .user_id import UserId
from .identity_invariants import (
    validate_email,
    normalize_display_name,
)


# ============================================================
# User Identity Aggregate (GA v1)
# ============================================================

@dataclass(frozen=True, slots=True)
class User(FrozenModel):
    """
    GA v1 User identity aggregate.

    Responsibilities:
    - Own identity attributes
    - Own lifecycle state (active/suspended)
    - Track role and permission assignments (DESCRIPTIVE only)

    Nonâ€‘Responsibilities:
    - Authorization decisions
    - Permission grammar enforcement
    - Policy evaluation
    """

    user_id: UserId
    tenant_id: TenantId

    email: str
    display_name: str

    active: bool

    # Descriptive only â€” RBAC consumes these
    roles: Tuple[RoleName, ...]
    direct_permissions: Tuple[str, ...]

    created_ms: UnixMillis
    updated_ms: UnixMillis

    # --------------------------------------------------------
    # Structural invariants (constructionâ€‘time)
    # --------------------------------------------------------

    def __post_init__(self) -> None:
        # Normalize identity fields
        object.__setattr__(self, "email", validate_email(self.email))
        object.__setattr__(
            self,
            "display_name",
            normalize_display_name(self.display_name),
        )

        if int(self.created_ms) < 0 or int(self.updated_ms) < 0:
            raise ValidationError(
                "timestamps must be non-negative",
                metadata={
                    "created_ms": int(self.created_ms),
                    "updated_ms": int(self.updated_ms),
                },
            )

        if int(self.updated_ms) < int(self.created_ms):
            raise ValidationError(
                "updated_ms cannot be earlier than created_ms",
                metadata={
                    "created_ms": int(self.created_ms),
                    "updated_ms": int(self.updated_ms),
                },
            )

        if any(r is None for r in self.roles):
            raise ValidationError(
                "roles must not contain None",
                metadata={"roles": self.roles},
            )

        if any(p is None for p in self.direct_permissions):
            raise ValidationError(
                "direct_permissions must not contain None",
                metadata={"direct_permissions": self.direct_permissions},
            )

    # --------------------------------------------------------
    # Guards (lifecycle / temporal invariants)
    # --------------------------------------------------------

    def ensure_active(self) -> "User":
        """
        Ensure the user is active.

        NOTE:
        - Used by higher layers before executing actions
        - This does NOT authorize anything
        """
        if not self.active:
            raise InvariantViolationError(
                "user is not active",
                metadata={"user_id": str(self.user_id)},
            )
        return self

    def _ensure_time_forward(self, now_ms: UnixMillis) -> None:
        if int(now_ms) < int(self.updated_ms):
            raise InvariantViolationError(
                "now_ms cannot be earlier than updated_ms",
                metadata={
                    "now_ms": int(now_ms),
                    "updated_ms": int(self.updated_ms),
                },
            )

    # --------------------------------------------------------
    # Pure state transitions
    # --------------------------------------------------------

    def activate(self, now_ms: UnixMillis) -> "User":
        self._ensure_time_forward(now_ms)
        if self.active:
            return replace(self, updated_ms=now_ms)
        return replace(self, active=True, updated_ms=now_ms)

    def deactivate(self, now_ms: UnixMillis) -> "User":
        self._ensure_time_forward(now_ms)
        if not self.active:
            return replace(self, updated_ms=now_ms)
        return replace(self, active=False, updated_ms=now_ms)

    def rename(self, display_name: str, now_ms: UnixMillis) -> "User":
        self._ensure_time_forward(now_ms)
        return replace(
            self,
            display_name=normalize_display_name(display_name),
            updated_ms=now_ms,
        )

    def change_email(self, email: str, now_ms: UnixMillis) -> "User":
        self._ensure_time_forward(now_ms)
        return replace(
            self,
            email=validate_email(email),
            updated_ms=now_ms,
        )

    def assign_role(self, role: RoleName, now_ms: UnixMillis) -> "User":
        self._ensure_time_forward(now_ms)
        if role in self.roles:
            return replace(self, updated_ms=now_ms)
        return replace(
            self,
            roles=self.roles + (role,),
            updated_ms=now_ms,
        )

    def revoke_role(self, role: RoleName, now_ms: UnixMillis) -> "User":
        self._ensure_time_forward(now_ms)
        if role not in self.roles:
            return replace(self, updated_ms=now_ms)
        return replace(
            self,
            roles=tuple(r for r in self.roles if r != role),
            updated_ms=now_ms,
        )

    def grant_permission(self, perm: str, now_ms: UnixMillis) -> "User":
        """
        Grant a direct permission (DESCRIPTIVE only).

        NOTE:
        - Permission grammar is validated by RBAC layer
        """
        self._ensure_time_forward(now_ms)
        if perm in self.direct_permissions:
            return replace(self, updated_ms=now_ms)
        return replace(
            self,
            direct_permissions=self.direct_permissions + (perm,),
            updated_ms=now_ms,
        )

    def revoke_permission(self, perm: str, now_ms: UnixMillis) -> "User":
        self._ensure_time_forward(now_ms)
        if perm not in self.direct_permissions:
            return replace(self, updated_ms=now_ms)
        return replace(
            self,
            direct_permissions=tuple(
                p for p in self.direct_permissions if p != perm
            ),
            updated_ms=now_ms,
        )

    # --------------------------------------------------------
    # Factory
    # --------------------------------------------------------

    @staticmethod
    def create(
        *,
        user_id: UserId,
        tenant_id: TenantId,
        email: str,
        display_name: str,
        now_ms: UnixMillis,
        roles: Tuple[RoleName, ...] = (),
        direct_permissions: Tuple[str, ...] = (),
        active: bool = True,
    ) -> "User":
        """
        Deterministic factory for GA v1 User identity.
        """
        return User(
            user_id=user_id,
            tenant_id=tenant_id,
            email=email,
            display_name=display_name,
            active=active,
            roles=tuple(roles),
            direct_permissions=tuple(direct_permissions),
            created_ms=now_ms,
            updated_ms=now_ms,
        )
