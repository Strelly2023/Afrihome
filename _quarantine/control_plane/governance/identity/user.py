from dataclasses import dataclass, replace
from typing import Tuple

from core.typing import UnixMillis, TenantId, RoleName
from core.errors import InvariantViolationError
from core.rbac.grammar import validate_permission_name

from .user_id import UserId
from .identity_invariants import validate_email, normalize_display_name


@dataclass(frozen=True, slots=True)
class User:
    """
    Immutable, tenant-scoped identity aggregate.

    - No I/O/ORM
    - All transitions are pure (return new instances)
    - Email & display name validated via identity_invariants
    - Role membership tracked by RoleName
    - Direct grants tracked by canonical permission names (not patterns)
    """
    user_id: UserId
    tenant_id: TenantId
    email: str
    display_name: str
    active: bool
    roles: Tuple[RoleName, ...]
    direct_permissions: Tuple[str, ...]
    created_ms: UnixMillis
    updated_ms: UnixMillis

    def __post_init__(self) -> None:
        e = validate_email(self.email)
        d = normalize_display_name(self.display_name)
        object.__setattr__(self, "email", e)
        object.__setattr__(self, "display_name", d)

        if int(self.created_ms) < 0 or int(self.updated_ms) < 0:
            raise InvariantViolationError("Timestamps must be non-negative")
        if int(self.updated_ms) < int(self.created_ms):
            raise InvariantViolationError("updated_ms cannot be earlier than created_ms")

        # Normalize permission names for direct grants
        if any(p is None for p in self.direct_permissions):
            raise InvariantViolationError("direct_permissions must not contain None")
        canon = tuple(validate_permission_name(p) for p in self.direct_permissions)
        object.__setattr__(self, "direct_permissions", canon)

    # ---------- Transitions (pure) ----------

    def ensure_active(self) -> "User":
        if not self.active:
            raise InvariantViolationError("User is not active")
        return self

    def activate(self, now_ms: UnixMillis) -> "User":
        return replace(self, active=True, updated_ms=now_ms)

    def deactivate(self, now_ms: UnixMillis) -> "User":
        return replace(self, active=False, updated_ms=now_ms)

    def rename(self, display_name: str, now_ms: UnixMillis) -> "User":
        d = normalize_display_name(display_name)
        return replace(self, display_name=d, updated_ms=now_ms)

    def change_email(self, email: str, now_ms: UnixMillis) -> "User":
        e = validate_email(email)
        return replace(self, email=e, updated_ms=now_ms)

    def assign_role(self, role: RoleName, now_ms: UnixMillis) -> "User":
        if role in self.roles:
            return replace(self, updated_ms=now_ms)
        return replace(self, roles=self.roles + (role,), updated_ms=now_ms)

    def revoke_role(self, role: RoleName, now_ms: UnixMillis) -> "User":
        if role not in self.roles:
            return replace(self, updated_ms=now_ms)
        new_roles = tuple(r for r in self.roles if r != role)
        return replace(self, roles=new_roles, updated_ms=now_ms)

    def grant_permission(self, perm_name: str, now_ms: UnixMillis) -> "User":
        p = validate_permission_name(perm_name)
        if p in self.direct_permissions:
            return replace(self, updated_ms=now_ms)
        return replace(self, direct_permissions=self.direct_permissions + (p,), updated_ms=now_ms)

    def revoke_permission(self, perm_name: str, now_ms: UnixMillis) -> "User":
        p = validate_permission_name(perm_name)
        if p not in self.direct_permissions:
            return replace(self, updated_ms=now_ms)
        new_perms = tuple(x for x in self.direct_permissions if x != p)
        return replace(self, direct_permissions=new_perms, updated_ms=now_ms)

    # ---------- Factory ----------

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
        # Validate via __post_init__ by constructing normalized values
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