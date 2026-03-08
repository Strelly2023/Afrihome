from dataclasses import dataclass
from typing import Tuple

from core.rbac.grammar import validate_permission_pattern, validate_role_name
from core.typing import RoleName


@dataclass(frozen=True, slots=True)
class Role:
    """
    Pure role value object (tenant-agnostic definition).

    - Name normalized via core.rbac.grammar
    - Patterns validated (e.g., "inventory.*", "orders.**")

    Notes:
    - This is a governance VO; evaluation lives in core.rbac or application.auth.
    - Use with deny-wins PolicyEngine when enforcing permissions.
    """

    name: RoleName
    allow: Tuple[str, ...] = ()
    deny: Tuple[str, ...] = ()

    def __post_init__(self) -> None:
        # Normalize role name
        rn = RoleName(validate_role_name(str(self.name)))
        object.__setattr__(self, "name", rn)

        # Normalize/validate patterns
        norm_allow = tuple(validate_permission_pattern(p) for p in self.allow)
        norm_deny = tuple(validate_permission_pattern(p) for p in self.deny)

        object.__setattr__(self, "allow", norm_allow)
        object.__setattr__(self, "deny", norm_deny)
