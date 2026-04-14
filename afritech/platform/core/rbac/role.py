from __future__ import annotations

"""
GA Enterprise Core â€” RBAC Role Definition
----------------------------------------

LAYER: L2 (Pure Engine)
Dependencies: core.rbac.grammar + core.typing + stdlib
Deterministic: YES
Side effects: NONE

Purpose:
- Define governance-level RBAC roles
- Represent allow/deny permission patterns declaratively

Rules:
- Pure value object
- No authorization or evaluation logic
- Grammar-validated
- Typed (no stringly-typed RBAC boundaries)
- No kernel or core.errors dependencies
"""

from dataclasses import dataclass
from typing import Tuple

from afritech.platform.core.typing import Permission, RoleName
from afritech.platform.core.rbac.grammar import (
    validate_role_name,
    validate_permission_pattern,
)


# ============================================================
# Role Definition (pure data, typed)
# ============================================================

@dataclass(frozen=True, slots=True)
class RoleDefinition:
    """
    GA v1 RBAC Role Definition.

    Represents a declarative mapping of permission *patterns*
    with deny-wins semantics evaluated by the RBAC engine.

    Notes:
    - `allow` and `deny` contain Permission patterns
    - Grammar and typing invariants are enforced at construction time
    - Evaluation semantics live in the RBAC policy engine
    """

    name: RoleName
    allow: Tuple[Permission, ...] = ()
    deny: Tuple[Permission, ...] = ()

    def __init__(
        self,
        *,
        name: str,
        allow: Tuple[str, ...] = (),
        deny: Tuple[str, ...] = (),
    ) -> None:
        # ----------------------------------------------------
        # Normalize and type role name
        # ----------------------------------------------------
        role_name: RoleName = validate_role_name(name)
        object.__setattr__(self, "name", role_name)

        # ----------------------------------------------------
        # Normalize and type permission patterns
        # ----------------------------------------------------
        typed_allow: Tuple[Permission, ...] = tuple(
            validate_permission_pattern(p) for p in allow
        )
        typed_deny: Tuple[Permission, ...] = tuple(
            validate_permission_pattern(p) for p in deny
        )

        object.__setattr__(self, "allow", typed_allow)
        object.__setattr__(self, "deny", typed_deny)


# ============================================================
# GA v1 Public Alias
# ============================================================

# In GA v1, Role is the canonical RBAC role type.
Role = RoleDefinition


# ============================================================
# RBAC Role ABI (explicit, frozen)
# ============================================================

__all__ = [
    "Role",
    "RoleDefinition",
]
