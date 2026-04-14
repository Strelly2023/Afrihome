from __future__ import annotations

"""
GA Enterprise Core â€” RBAC Policy Engine (Denyâ€‘Wins)
--------------------------------------------------

LAYER: L2 (Pure Engine)
Dependencies:
- core.rbac.role
- core.rbac.permission
- core.typing
- stdlib

Deterministic: YES
Side effects: NONE
IO / Time / Network: NONE

Purpose:
- Evaluate RBAC permission requests using denyâ€‘wins semantics
- Produce deterministic, replayâ€‘safe authorization decisions

Rules:
- Pure evaluation only (no persistence, no resolution)
- No kernel or L1 foundation dependencies
- Typed RBAC boundaries (no stringlyâ€‘typed permissions or roles)
- Structural misuse MUST be caught before engine entry
"""

from dataclasses import dataclass
from typing import Mapping, Optional, Tuple, Iterable

from afritech.platform.core.typing import Permission, RoleName
from afritech.platform.core.rbac.role import RoleDefinition
from afritech.platform.core.rbac.permission import permission_matches


# ============================================================
# RBAC Core Models (Typed, Pure)
# ============================================================

@dataclass(frozen=True, slots=True)
class Subject:
    """
    Actor attempting to perform an action.

    Attributes:
    - roles: Tuple of RoleName assigned to the subject
    """

    roles: Tuple[RoleName, ...]


@dataclass(frozen=True, slots=True)
class Policy:
    """
    RBAC policy definition.

    Attributes:
    - roles: Mapping RoleName â†’ RoleDefinition
    """

    roles: Mapping[RoleName, RoleDefinition]

    def role_for(self, role_name: RoleName) -> Optional[RoleDefinition]:
        """
        Safe role lookup.

        Missing roles are ignored (failâ€‘safe).
        """
        return self.roles.get(role_name)


@dataclass(frozen=True, slots=True)
class Decision:
    """
    Result of RBAC policy evaluation.

    Invariants:
    - `allowed` is authoritative
    - `reason` is deterministic and stable
    """

    allowed: bool
    reason: str
    role: Optional[RoleName] = None
    pattern: Optional[Permission] = None


# ============================================================
# Policy Engine (Pure, Denyâ€‘Wins)
# ============================================================

class PolicyEngine:
    """
    Deterministic RBAC evaluation engine.

    Properties:
    - Pure function behavior
    - Denyâ€‘wins semantics
    - No external state
    """

    def _roles_for_subject(
        self,
        *,
        policy: Policy,
        subject: Subject,
    ) -> Iterable[RoleDefinition]:
        """
        Resolve concrete RoleDefinition objects assigned to a subject.

        Missing or unknown roles are ignored (failâ€‘safe).
        """
        for role_name in subject.roles:
            role = policy.role_for(role_name)
            if role is not None:
                yield role

    def evaluate(
        self,
        *,
        policy: Policy,
        subject: Subject,
        permission: Permission,
    ) -> Decision:
        """
        Evaluate a permission request.

        Deterministic, sideâ€‘effect free, idempotent.

        Notes:
        - Structural validation is assumed upstream
        - This engine NEVER raises for allow/deny outcomes
        """

        roles = tuple(
            self._roles_for_subject(
                policy=policy,
                subject=subject,
            )
        )

        # -------------------------------------------------
        # PASS 1 â€” DENY RULES (denyâ€‘wins)
        # -------------------------------------------------

        for role in roles:
            for pattern in role.deny:
                if permission_matches(pattern, permission):
                    return Decision(
                        allowed=False,
                        reason="deny:matched_deny_rule",
                        role=role.name,
                        pattern=pattern,
                    )

        # -------------------------------------------------
        # PASS 2 â€” ALLOW RULES
        # -------------------------------------------------

        for role in roles:
            for pattern in role.allow:
                if permission_matches(pattern, permission):
                    return Decision(
                        allowed=True,
                        reason="allow:matched_allow_rule",
                        role=role.name,
                        pattern=pattern,
                    )

        # -------------------------------------------------
        # DEFAULT DENY (failâ€‘safe)
        # -------------------------------------------------

        return Decision(
            allowed=False,
            reason="deny:default",
        )


# ============================================================
# Functional API (pure helper)
# ============================================================

_ENGINE = PolicyEngine()


def evaluate(
    *,
    policy: Policy,
    subject: Subject,
    permission: Permission,
) -> Decision:
    """
    Functional entrypoint for RBAC evaluation.
    """
    return _ENGINE.evaluate(
        policy=policy,
        subject=subject,
        permission=permission,
    )


# ============================================================
# RBAC Policy Engine ABI (explicit, frozen)
# ============================================================

__all__ = [
    "Subject",
    "Policy",
    "Decision",
    "PolicyEngine",
    "evaluate",
]
