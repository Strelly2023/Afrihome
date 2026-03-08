from __future__ import annotations

import re
from typing import Final

from core.errors import GrammarViolationError

from .permission import validate_permission_name

_SEG: Final[str] = r"[a-z][a-z0-9]*"
# pattern tokens: literal SEG, '*', '**'
_PATTERN_RE: Final[re.Pattern[str]] = re.compile(rf"^(?:{_SEG}|\*|\*\*)(?:\.(?:{_SEG}|\*|\*\*))*$")


def _normalize(s: str, *, field: str) -> str:
    if s is None:
        raise GrammarViolationError(f"{field} must not be None")
    t = s.strip().lower()
    if not t:
        raise GrammarViolationError(f"{field} must not be empty")
    return t


def validate_permission_pattern(pattern: str) -> str:
    p = _normalize(pattern, field="permission pattern")
    if not _PATTERN_RE.match(p):
        raise GrammarViolationError(f"Invalid permission pattern: {pattern!r}")
    # '**' only as the last segment
    tokens = p.split(".")
    for i, tok in enumerate(tokens):
        if tok == "**" and i != len(tokens) - 1:
            raise GrammarViolationError("The '**' wildcard is only allowed as the last segment")
    return p


def permission_matches(pattern: str, name: str) -> bool:
    """
    Segment-wise matcher:
      • '*'  matches exactly one segment
      • '**' matches zero or more trailing segments (must be last token)
    """
    p = validate_permission_pattern(pattern)
    n = validate_permission_name(name)

    ptoks = p.split(".")
    ntoks = n.split(".")

    i = j = 0
    while i < len(ptoks) and j < len(ntoks):
        seg = ptoks[i]
        if seg == "**":
            return i == len(ptoks) - 1
        if seg == "*":
            i += 1
            j += 1
            continue
        if seg != ntoks[j]:
            return False
        i += 1
        j += 1

    if i == len(ptoks):
        return j == len(ntoks)
    return (i == len(ptoks) - 1) and (ptoks[i] == "**")
