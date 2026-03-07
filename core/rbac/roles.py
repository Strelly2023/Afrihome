
"""
GA Enterprise Core — RBAC Role Model (Immutable)
------------------------------------------------

LAYER: L3
Dependencies:
- core.typing (RoleName)
- core.rbac.grammar
- core.kernel.invariants

No tenancy import: ENFORCED
"""


from dataclasses import dataclass
from typing import Tuple

from core.typing import RoleName
from core.rbac.grammar import validate_role_name, validate_permission_pattern


@dataclass(frozen=True, slots=True)
class Role:
    name: RoleName
    allow: Tuple[str, ...] = ()
    deny: Tuple[str, ...] = ()

    def __post_init__(self) -> None:
        n = validate_role_name(str(self.name))
        object.__setattr__(self, "name", RoleName(n))
        norm_allow = tuple(validate_permission_pattern(p) for p in self.allow)
        norm_deny = tuple(validate_permission_pattern(p) for p in self.deny)
        object.__setattr__(self, "allow", norm_allow)
        object.__setattr__(self, "deny", norm_deny)
