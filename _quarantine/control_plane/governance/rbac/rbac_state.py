from dataclasses import dataclass, field, replace
from typing import Dict, Tuple, Optional

from core.typing import RoleName, Permission, UserId
from core.errors import InvariantViolationError
from core.rbac.roles import Role as CoreRole
from core.rbac.policy_engine import Policy, Subject, PolicyEngine


from .role import RoleDefinition


@dataclass(frozen=True, slots=True)
class RBACState:
    """
    Immutable RBAC registry + assignments.

    - roles: mapping of role_name -> RoleDefinition (definition registry)
    - assignments: mapping of user_id -> tuple[RoleName, ...] (who has what roles)
    - Pure updates (return new RBACState)
    - Deterministic evaluation via core.rbac.PolicyEngine (deny-wins)

    Scope:
    - This object can be logically tenant-scoped by its owner.
      We keep it tenant-agnostic here to remain reusable.
    """
    roles: Dict[str, RoleDefinition] = field(default_factory=dict)
    assignments: Dict[str, Tuple[RoleName, ...]] = field(default_factory=dict)

    # ---------- Role Registry (pure) ----------

    def register_role(self, role: RoleDefinition) -> "RBACState":
        name = str(role.name)
        if name in self.roles:
            raise InvariantViolationError(f"Role {name!r} already exists")
        new_roles = dict(self.roles)
        new_roles[name] = role
        return replace(self, roles=new_roles)

    def upsert_role(self, role: RoleDefinition) -> "RBACState":
        name = str(role.name)
        new_roles = dict(self.roles)
        new_roles[name] = role
        return replace(self, roles=new_roles)

    def remove_role(self, role_name: RoleName) -> "RBACState":
        name = str(role_name)
        if name not in self.roles:
            raise InvariantViolationError(f"Role {name!r} not found")
        # Remove role definition
        new_roles = dict(self.roles)
        del new_roles[name]
        # Remove role from assignments
        new_assignments: Dict[str, Tuple[RoleName, ...]] = {}
        for uid, roles in self.assignments.items():
            new_assignments[uid] = tuple(r for r in roles if str(r) != name)
        return replace(self, roles=new_roles, assignments=new_assignments)

    # ---------- Assignments (pure) ----------

    def assign_role(self, user_id: UserId, role_name: RoleName) -> "RBACState":
        rname = str(role_name)
        if rname not in self.roles:
            raise InvariantViolationError(f"Role {rname!r} is not registered")
        uid = str(user_id)
        current = self.assignments.get(uid, ())
        if role_name in current:
            return replace(self, assignments=dict(self.assignments))  # no-op; preserve immutability
        new_assignments = dict(self.assignments)
        new_assignments[uid] = current + (role_name,)
        return replace(self, assignments=new_assignments)

    def revoke_role(self, user_id: UserId, role_name: RoleName) -> "RBACState":
        uid = str(user_id)
        current = self.assignments.get(uid)
        if not current:
            return replace(self, assignments=dict(self.assignments))
        new = tuple(r for r in current if r != role_name)
        new_assignments = dict(self.assignments)
        new_assignments[uid] = new
        return replace(self, assignments=new_assignments)

    def subject_roles(self, user_id: UserId) -> Tuple[RoleName, ...]:
        return self.assignments.get(str(user_id), ())

    # ---------- Evaluation (deny-wins, deterministic) ----------

    def _to_policy(self) -> Policy:
        """
        Convert RoleDefinition registry to a core.rbac.policy_engine.Policy.
        Deterministic mapping: copy allow/deny exactly as defined.
        """
        roles_map: Dict[str, CoreRole] = {
            name: CoreRole(name=RoleName(name), allow=tuple(defn.allow), deny=tuple(defn.deny))
            for name, defn in self.roles.items()
        }
        return Policy(roles=roles_map)

    def evaluate_for_user(self, user_id: UserId, permission: Permission) -> bool:
        """
        Deny-wins permission check for a given user_id and permission name.
        Returns True if allowed, False otherwise.
        """
        policy = self._to_policy()
        subject = Subject(user_id=user_id, roles=self.subject_roles(user_id))
        decision = PolicyEngine().evaluate(policy, subject, permission)
        return decision.allowed

    def debug_decision(self, user_id: UserId, permission: Permission) -> str:
        """
        Same as evaluate_for_user, but returns reason string for diagnostics.
        """
        policy = self._to_policy()
        subject = Subject(user_id=user_id, roles=self.subject_roles(user_id))
        decision = PolicyEngine().evaluate(policy, subject, permission)
        return decision.reason