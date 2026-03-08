from dataclasses import dataclass
from typing import Tuple

from core.rbac.grammar import (
    validate_permission_pattern,  # single permission grammar authority  # noqa
)


@dataclass(frozen=True, slots=True)
class ApiKeyScope:
    """
    Permission patterns granted to this key (deny-wins is enforced by RBAC engine later).
    Patterns validated through the single RBAC grammar authority.
    """

    allow: Tuple[str, ...] = ()
    deny: Tuple[str, ...] = ()

    def __post_init__(self) -> None:
        norm_allow = tuple(validate_permission_pattern(p) for p in (self.allow or ()))
        norm_deny = tuple(validate_permission_pattern(p) for p in (self.deny or ()))
        object.__setattr__(self, "allow", norm_allow)
        object.__setattr__(self, "deny", norm_deny)
