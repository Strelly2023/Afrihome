from dataclasses import dataclass
from typing import Tuple

from core.typing import RoleName
from core.rbac.grammar import validate_role_name, validate_permission_pattern


@dataclass(frozen=True, slots=True)
class RoleDefinition:
    """
    Governance-level Role definition.

    - Name normalized by core.rbac.grammar.validate_role_name
    - Allow/Deny patterns normalized by validate_permission_pattern
    - Immutable VO (definition only; no enforcement here)

    Notes:
    - Use with RBACState to build a per-tenant (or per-scope) registry
    - Application/authorization composes this with core.rbac.PolicyEngine
    """
    name: RoleName
    allow: Tuple[str, ...] = ()
    deny: Tuple[str, ...] = ()

    def __post_init__(self) -> None:
        rn = RoleName(validate_role_name(str(self.name)))
        object.__setattr__(self, "name", rn)

        norm_allow = tuple(validate_permission_pattern(p) for p in self.allow)
        norm_deny = tuple(validate_permission_pattern(p) for p in self.deny)

        object.__setattr__(self, "allow", norm_allow)
        object.__setattr__(self, "deny", norm_deny)