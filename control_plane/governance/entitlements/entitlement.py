# control_plane/governance/entitlements/entitlement.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from core.errors import GrammarViolationError


@dataclass(frozen=True)
class Entitlement:
    """
    A single entitlement for a feature or capability.

    Examples
    --------
    - key="storage.gb",     limit=100,  is_unlimited=False
    - key="projects.count", limit=None, is_unlimited=True   (unlimited)

    Notes
    -----
    - `limit=None` implies unlimited quota.
    - If `is_unlimited=True`, `limit` MUST be None (enforced).
    """

    key: str
    limit: Optional[int]  # None => unlimited
    is_unlimited: bool

    def __post_init__(self) -> None:
        k = (self.key or "").strip().lower()
        if not k:
            raise GrammarViolationError("entitlement key must not be empty")

        if self.limit is not None and self.limit < 0:
            raise GrammarViolationError("entitlement limit cannot be negative")

        if self.is_unlimited and self.limit is not None:
            raise GrammarViolationError("unlimited entitlements cannot have numeric limit")

        object.__setattr__(self, "key", k)
