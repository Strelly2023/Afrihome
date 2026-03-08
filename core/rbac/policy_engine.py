"""
GA Enterprise Core — RBAC Policy Engine (Deny-Wins)
---------------------------------------------------

LAYER: L3
Dependencies:
- core.rbac.roles
- core.rbac.permissions
- core.typing
- core.kernel.invariants

Deterministic: YES
No tenancy imports: ENFORCED
"""

from dataclasses import dataclass
from typing import Dict, Optional, Tuple

from core.kernel.invariants import assert_not_none
from core.rbac.permissions import permission_matches
from core.rbac.roles import Role
from core.typing import Permission, RoleName, UserId


@dataclass(frozen=True, slots=True)
class Subject:
    user_id: Optional[UserId]
    roles: Tuple[RoleName, ...]


@dataclass(frozen=True, slots=True)
class Policy:
    """
    Immutable RBAC policy.
    """

    roles: Dict[RoleName, Role]


@dataclass(frozen=True, slots=True)
class Decision:
    allowed: bool
    reason: str
    role: Optional[RoleName] = None
    pattern: Optional[str] = None


class PolicyEngine:
    """
    Deterministic RBAC evaluation.

    Algorithm
    ----------
    1. Resolve subject roles
    2. Evaluate DENY rules (deny-wins)
    3. Evaluate ALLOW rules
    4. Default deny

    Properties
    ----------
    - deterministic
    - side-effect free
    - stable role ordering
    """

    __slots__ = ()

    def _resolve_roles(
        self,
        policy: Policy,
        subject: Subject,
    ) -> Tuple[Role, ...]:

        roles = policy.roles

        resolved: list[Role] = []

        for rn in subject.roles:
            role = roles.get(rn)
            if role is not None:
                resolved.append(role)

        return tuple(resolved)

    def evaluate(
        self,
        policy: Policy,
        subject: Subject,
        permission: Permission,
    ) -> Decision:

        assert_not_none(policy, "policy")
        assert_not_none(subject, "subject")
        assert_not_none(permission, "permission")

        perm = str(permission)

        roles = self._resolve_roles(policy, subject)

        # ---- DENY PASS ----
        for role in roles:
            for pat in role.deny:
                if permission_matches(pat, perm):
                    return Decision(
                        allowed=False,
                        reason=f"deny: role={role.name} pattern={pat}",
                        role=role.name,
                        pattern=pat,
                    )

        # ---- ALLOW PASS ----
        for role in roles:
            for pat in role.allow:
                if permission_matches(pat, perm):
                    return Decision(
                        allowed=True,
                        reason=f"allow: role={role.name} pattern={pat}",
                        role=role.name,
                        pattern=pat,
                    )

        return Decision(
            allowed=False,
            reason="deny: default",
        )


def evaluate(
    policy: Policy,
    subject: Subject,
    permission: Permission,
) -> Decision:
    """
    Functional RBAC evaluation API.
    """
    return PolicyEngine().evaluate(policy, subject, permission)
