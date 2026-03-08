# control_plane/governance/rbac/rbac_state.py
from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Dict, Iterable, Mapping, Tuple

from control_plane.governance.identity.user_id import UserId
from core.errors import GrammarViolationError

from .permission import Permission  # for evaluate_for_user back-compat
from .role import Role, RoleName, _norm_role
from .role_binding import RoleBinding


def _norm_user_id(uid: str) -> str:
    if uid is None:
        raise GrammarViolationError("user_id must not be None")
    u = uid.strip()
    if not u:
        raise GrammarViolationError("user_id must not be empty")
    return u


@dataclass(frozen=True)
class RBACState:
    """
    Immutable RBAC snapshot:

      - roles:       role_name -> Role (allow/deny patterns)
      - assignments: user_id   -> tuple(role_name, ...)

    Deny-wins evaluation:
      1) If ANY assigned role denies => DENY
      2) Else if ANY assigned role allows => ALLOW
      3) Else => default DENY
    """

    roles: Mapping[str, Role] = field(default_factory=dict)
    assignments: Mapping[str, Tuple[str, ...]] = field(
        default_factory=dict
    )  # user_id -> role names

    # ---------------- Canonical immutable builders ----------------

    def with_role(self, role: Role) -> "RBACState":
        rname = role.name
        new_roles: Dict[str, Role] = dict(self.roles)
        new_roles[rname] = role
        return replace(self, roles=new_roles)

    def without_role(self, role_name: str) -> "RBACState":
        rn = _norm_role(role_name)
        if rn not in self.roles:
            return self
        new_roles: Dict[str, Role] = dict(self.roles)
        del new_roles[rn]
        new_asg: Dict[str, Tuple[str, ...]] = {
            uid: tuple(r for r in roles if r != rn) for uid, roles in self.assignments.items()
        }
        return replace(self, roles=new_roles, assignments=new_asg)

    def assign(self, user_id: str, *role_names: str) -> "RBACState":
        uid = _norm_user_id(user_id)
        rs = tuple(_norm_role(r) for r in role_names)
        cur = tuple(self.assignments.get(uid, ()))
        seen = set(cur)
        merged = cur + tuple(r for r in rs if r not in seen)
        return replace(self, assignments={**self.assignments, uid: merged})

    def unassign(self, user_id: str, role_name: str) -> "RBACState":
        uid = _norm_user_id(user_id)
        rn = _norm_role(role_name)
        cur = tuple(self.assignments.get(uid, ()))
        if rn not in cur:
            return self
        new_tuple = tuple(r for r in cur if r != rn)
        new_asg = dict(self.assignments)
        new_asg[uid] = new_tuple
        return replace(self, assignments=new_asg)

    # ---------------- Back-compat shims ----------------

    def register_role(self, role: Role) -> "RBACState":
        return self.with_role(role)

    def register_roles(self, *roles: Role) -> "RBACState":
        s = self
        for r in roles:
            s = s.with_role(r)
        return s

    def register_binding(self, binding: RoleBinding) -> "RBACState":
        return self.assign(binding.user_id, *binding.roles)

    def assign_user(self, user_id: str | UserId, roles: Iterable[str]) -> "RBACState":
        uid = str(user_id) if isinstance(user_id, UserId) else _norm_user_id(user_id)
        canon = tuple(_norm_role(r) for r in roles or ())
        if not canon:
            return self
        return self.assign(uid, *canon)

    def unassign_user(self, user_id: str | UserId, role_name: str) -> "RBACState":
        uid = str(user_id) if isinstance(user_id, UserId) else _norm_user_id(user_id)
        return self.unassign(uid, role_name)

    def roles_of(self, user_id: str | UserId) -> Tuple[str, ...]:
        return self.roles_for_user(user_id)

    def assign_role(self, user_id: str | UserId, role_name: str | RoleName) -> "RBACState":
        """
        Back-compat single-role assign:
          - user_id may be UserId or str
          - role_name may be RoleName or str
        """
        uid = str(user_id) if isinstance(user_id, UserId) else _norm_user_id(user_id)
        rn = str(role_name) if isinstance(role_name, RoleName) else role_name
        return self.assign(uid, rn)

    # ---------------- Queries / evaluation ----------------

    def roles_for_user(self, user_id: str | UserId) -> Tuple[str, ...]:
        uid = str(user_id) if isinstance(user_id, UserId) else _norm_user_id(user_id)
        return tuple(self.assignments.get(uid, ()))

    def has_for_user(self, user_id: str | UserId, permission: str) -> bool:
        uid = str(user_id) if isinstance(user_id, UserId) else _norm_user_id(user_id)
        names = self.assignments.get(uid, ())
        if not names:
            return False
        roles = [self.roles[rn] for rn in names if rn in self.roles]
        if any(r.denies(permission) for r in roles):  # deny wins
            return False
        if any(r.allows(permission) for r in roles):
            return True
        return False

    def evaluate_for_user(self, user_id: str | UserId, permission: str | Permission) -> bool:
        """
        Back-compat alias for has_for_user(...), accepting either a raw permission string
        or a Permission value object.
        """
        perm_name = permission.name if isinstance(permission, Permission) else str(permission)
        return self.has_for_user(user_id, perm_name)

    def reason_for_user(self, user_id: str | UserId, permission: str) -> str:
        uid = str(user_id) if isinstance(user_id, UserId) else _norm_user_id(user_id)
        names = self.assignments.get(uid, ())
        roles = [self.roles[rn] for rn in names if rn in self.roles]
        if not roles:
            return "deny: default (no roles)"
        for r in roles:
            if r.denies(permission):
                return f"deny: role {r.name}"
        for r in roles:
            if r.allows(permission):
                return f"allow: role {r.name}"
        return "deny: default"
