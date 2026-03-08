# control_plane/governance/rbac/role_binding.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from .role import _norm_role


@dataclass(frozen=True)
class RoleBinding:
    user_id: str
    roles: Tuple[str, ...]  # role names

    def __post_init__(self) -> None:
        uid = (self.user_id or "").strip()
        if not uid:
            raise ValueError("user_id must not be empty")
        object.__setattr__(self, "user_id", uid)
        object.__setattr__(self, "roles", tuple(_norm_role(r) for r in (self.roles or ())))
