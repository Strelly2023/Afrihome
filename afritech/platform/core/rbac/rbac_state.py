from __future__ import annotations
#afritech/platform/core/rbac/rbac_state.py
"""
GA Enterprise Core â€” RBAC State
-------------------------------

LAYER: L2 (Pure Engine)
Dependencies:
- core.rbac.role
- core.rbac.policy_engine
- core.rbac.errors
- core.typing
- stdlib

Deterministic: YES
Side effects: NONE
IO / Time / Network: NONE

Purpose:
- Represent an immutable RBAC registry and role assignments
- Bridge RBAC data to the RBAC PolicyEngine for evaluation

Rules:
- Pure value state only
- No kernel or L1 foundation dependencies
- Fail-safe semantics (unknown roles ignored)
- Typed RBAC boundaries (no stringly-typed permissions or roles)
"""

from dataclasses import dataclass, replace
from types import MappingProxyType
from typing import Mapping, Tuple

from afritech.platform.core.typing import Permission, RoleName
from afritech.platform.core.rbac.role import RoleDefinition
from afritech.platform.core.rbac.policy_engine import (
    Policy,
    Subject,
    evaluate,
)
from afritech.platform.core.rbac.errors import (
    RoleAlreadyExistsError,
    RoleNotFoundError,
    InvalidRoleAssignmentError,
)


# ============================================================
# RBAC State (immutable snapshot)
# ============================================================

@dataclass(frozen=True, slots=True)
class RBACState:
    """
    Immutable RBAC registry and role assignments.

    Invariants:
    - `roles` maps RoleName â†’ RoleDefinition
    - `assignments` maps subject_id â†’ Tuple[RoleName, ...]
    - Unknown roles in assignments are ignored (fail-safe)
    """

    roles: Mapping[RoleName, RoleDefinition]
    assignments: Mapping[str, Tuple[RoleName, ...]]

    # --------------------------------------------------------
    # Structural normalization (immutability + fail-safe)
    # --------------------------------------------------------

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "roles",
            MappingProxyType(dict(self.roles)),
        )

        normalized_assignments = {
            subject_id: tuple(
                role
                for role in role_names
                if role in self.roles
            )
            for subject_id, role_names in self.assignments.items()
        }

        object.__setattr__(
            self,
            "assignments",
            MappingProxyType(normalized_assignments),
        )

    # --------------------------------------------------------
    # Role registry
    # --------------------------------------------------------

    def register_role(self, role: RoleDefinition) -> "RBACState":
        """
        Register a new role.

        Raises:
            RoleAlreadyExistsError if role already exists.
        """
        if role.name in self.roles:
            raise RoleAlreadyExistsError(role_name=role.name)

        new_roles = dict(self.roles)
        new_roles[role.name] = role
        return replace(self, roles=new_roles)

    def upsert_role(self, role: RoleDefinition) -> "RBACState":
        """
        Insert or replace a role definition.
        """
        new_roles = dict(self.roles)
        new_roles[role.name] = role
        return replace(self, roles=new_roles)

    def remove_role(self, role_name: RoleName) -> "RBACState":
        """
        Remove a role and revoke it from all subjects.
        """
        if role_name not in self.roles:
            raise RoleNotFoundError(role_name=role_name)

        new_roles = dict(self.roles)
        new_roles.pop(role_name)

        new_assignments = {
            subject_id: tuple(
                r for r in role_names if r != role_name
            )
            for subject_id, role_names in self.assignments.items()
        }

        return replace(
            self,
            roles=new_roles,
            assignments=new_assignments,
        )

    # --------------------------------------------------------
    # Assignments (fail-safe)
    # --------------------------------------------------------

    def assign_role(
        self,
        *,
        subject_id: str,
        role_name: RoleName,
    ) -> "RBACState":
        """
        Assign a role to a subject.

        Fail-safe semantics:
        - Unknown role â‡’ no-op
        """
        if role_name not in self.roles:
            return self

        current = self.assignments.get(subject_id, ())
        if role_name in current:
            return self

        new_assignments = dict(self.assignments)
        new_assignments[subject_id] = current + (role_name,)
        return replace(self, assignments=new_assignments)

    def revoke_role(
        self,
        *,
        subject_id: str,
        role_name: RoleName,
    ) -> "RBACState":
        """
        Revoke a role from a subject.
        """
        current = self.assignments.get(subject_id)
        if not current:
            return self

        new_assignments = dict(self.assignments)
        new_assignments[subject_id] = tuple(
            r for r in current if r != role_name
        )
        return replace(self, assignments=new_assignments)

    def subject_roles(self, subject_id: str) -> Tuple[RoleName, ...]:
        """
        Return roles assigned to a subject.
        """
        return self.assignments.get(subject_id, ())

    # --------------------------------------------------------
    # Evaluation
    # --------------------------------------------------------

    def _to_policy(self) -> Policy:
        return Policy(roles=self.roles)

    def evaluate_for_subject(
        self,
        *,
        subject_id: str,
        permission: Permission,
    ) -> bool:
        """
        Evaluate whether a subject has a permission.
        """
        policy = self._to_policy()
        subject = Subject(roles=self.subject_roles(subject_id))
        return evaluate(
            policy=policy,
            subject=subject,
            permission=permission,
        ).allowed

    def debug_decision(
        self,
        *,
        subject_id: str,
        permission: Permission,
    ) -> str:
        """
        Return decision reason for debugging / audit.
        """
        policy = self._to_policy()
        subject = Subject(roles=self.subject_roles(subject_id))
        return evaluate(
            policy=policy,
            subject=subject,
            permission=permission,
        ).reason

    # --------------------------------------------------------
    # Compatibility alias (GA v1)
    # --------------------------------------------------------

    def has_for_subject(
        self,
        *,
        subject_id: str,
        permission: Permission,
    ) -> bool:
        """
        Backwards-compatible alias.
        """
        return self.evaluate_for_subject(
            subject_id=subject_id,
            permission=permission,
        )


# ============================================================
# Public ABI (explicit, frozen)
# ============================================================

__all__ = [
    "RBACState",
]
