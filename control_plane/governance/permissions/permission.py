from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Final

from core.errors import GrammarViolationError

_SEG: Final[str] = r"[a-z][a-z0-9]*"
_PERMISSION_NAME_RE: Final[re.Pattern[str]] = re.compile(rf"^{_SEG}(?:\.{_SEG})*$")


def _normalize(s: str, *, field: str) -> str:
    if s is None:
        raise GrammarViolationError(f"{field} must not be None")
    t = s.strip().lower()
    if not t:
        raise GrammarViolationError(f"{field} must not be empty")
    return t


def validate_permission_name(name: str) -> str:
    n = _normalize(name, field="permission name")
    if not _PERMISSION_NAME_RE.match(n):
        raise GrammarViolationError(f"Invalid permission name: {name!r}")
    return n


@dataclass(frozen=True)
class Permission:
    name: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "name", validate_permission_name(self.name))
