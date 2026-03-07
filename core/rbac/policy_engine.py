
"""
GA Enterprise Core — RBAC Policy Engine (Deny-Wins)
---------------------------------------------------

LAYER: L3
Dependencies:
- core.rbac.roles
- core.rbac.permissions
- core.typing
- core.kernel.invariants
- core.errors

Deterministic: YES
No tenancy imports: ENFORCED
"""


from dataclasses import dataclass
from typing import Dict, Tuple, Optional

from core.rbac.roles import Role
from core.rbac.permissions import permission_matches
from core.typing import RoleName, Permission, UserId
from core.kernel.invariants import assert_not_none


@dataclass(frozen=True, slots=True)
class Subject:
    user_id: Optional[UserId]
    roles: Tuple[RoleName, ...]


@dataclass(frozen=True, slots=True)
class Policy:
    roles: Dict[str, Role]


@dataclass(frozen=True, slots=True)
class Decision:
    allowed: bool
    reason: str
    role: Optional[RoleName] = None
    pattern: Optional[str] = None


class PolicyEngine:
    def evaluate(self, policy: Policy, subject: Subject, permission: Permission) -> Decision:
        assert_not_none(policy, "policy")
        assert_not_none(subject, "subject")
        assert_not_none(permission, "permission")
        perm = str(permission)
        for rn in subject.roles:
            role = policy.roles.get(str(rn))
            if role is None:
                continue
            for pat in role.deny:
                if permission_matches(pat, perm):
                    return Decision(allowed=False, reason=f"deny: role={str(role.name)} pattern={pat}", role=RoleName(str(role.name)), pattern=pat)
        for rn in subject.roles:
            role = policy.roles.get(str(rn))
            if role is None:
                continue
            for pat in role.allow:
                if permission_matches(pat, perm):
                    return Decision(allowed=True, reason=f"allow: role={str(role.name)} pattern={pat}", role=RoleName(str(role.name)), pattern=pat)
        return Decision(allowed=False, reason="deny: default")


def evaluate(policy: Policy, subject: Subject, permission: Permission) -> Decision:
    return PolicyEngine().evaluate(policy, subject, permission)
