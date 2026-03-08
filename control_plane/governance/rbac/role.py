# control_plane/governance/rbac/role.py
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Final, Tuple

from core.errors import GrammarViolationError

# Recommended: import from the split permissions module
from ..permissions.pattern import permission_matches, validate_permission_pattern

# If you kept permissions embedded under RBAC for now, use this instead:
# from .permission import validate_permission_pattern, permission_matches

ROLE_NAME_RE: Final[re.Pattern[str]] = re.compile(r"^[a-z][a-z0-9]*(?:[._-][a-z0-9]+)*$")


def _norm_role(name: str) -> str:
    if name is None:
        raise GrammarViolationError("Role name must not be None")
    n = name.strip().lower()
    if not n:
        raise GrammarViolationError("Role name must not be empty")
    if not ROLE_NAME_RE.match(n):
        raise GrammarViolationError(f"Invalid role name: {name!r}")
    return n


@dataclass(frozen=True)
class RoleName:
    value: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "value", _norm_role(self.value))

    def __str__(self) -> str:  # lets str(RoleName("admin")) == "admin"
        return self.value


@dataclass(frozen=True)
class Role:
    """
    Pure role definition with allow/deny patterns.
    Deny-wins semantics is enforced during evaluation.
    """

    # Accept str or RoleName for back-compat
    name: Any
    allow: Tuple[str, ...] = ()
    deny: Tuple[str, ...] = ()

    def __post_init__(self) -> None:
        # Coerce name to canonical string
        raw = str(self.name) if not isinstance(self.name, str) else self.name
        rn = _norm_role(raw)

        # Validate patterns deterministically
        a = tuple(validate_permission_pattern(x) for x in (self.allow or ()))
        d = tuple(validate_permission_pattern(x) for x in (self.deny or ()))

        object.__setattr__(self, "name", rn)
        object.__setattr__(self, "allow", a)
        object.__setattr__(self, "deny", d)

    # ---------- Evaluation helpers (pure) ----------
    def denies(self, perm: str) -> bool:
        return any(permission_matches(p, perm) for p in self.deny)

    def allows(self, perm: str) -> bool:
        return any(permission_matches(p, perm) for p in self.allow)


# Back-compat alias used in some tests/call-sites
RoleDefinition = Role
