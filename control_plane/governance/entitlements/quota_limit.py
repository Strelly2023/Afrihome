# control_plane/governance/entitlements/quota_limit.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from core.errors import GrammarViolationError


@dataclass(frozen=True)
class QuotaLimit:
    """
    A generic numeric quota, e.g., 'api.calls.per_month'.
    """

    amount: Optional[int]  # None => unlimited

    def __post_init__(self) -> None:
        if self.amount is not None and self.amount < 0:
            raise GrammarViolationError("Quota amount must be >= 0")

    def is_unlimited(self) -> bool:
        return self.amount is None
