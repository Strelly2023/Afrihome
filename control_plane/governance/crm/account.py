# control_plane/governance/crm/account.py
from dataclasses import dataclass, replace
from typing import Any, Dict, Mapping, Optional

from core.errors import InvariantViolationError

from .crm_invariants import (
    normalize_email,
    normalize_id,
    normalize_metadata,
    normalize_name,
    normalize_phone,
)


@dataclass(frozen=True)
class Account:
    """
    A tenant-scoped business account (B2B/B2C), pure and deterministic.
    """

    account_id: str
    name: str
    primary_email: Optional[str]
    primary_phone: Optional[str]
    metadata: Dict[str, Any]

    def __post_init__(self) -> None:
        object.__setattr__(self, "account_id", normalize_id(self.account_id))
        object.__setattr__(self, "name", normalize_name(self.name))
        object.__setattr__(self, "primary_email", normalize_email(self.primary_email))
        object.__setattr__(self, "primary_phone", normalize_phone(self.primary_phone))
        object.__setattr__(self, "metadata", normalize_metadata(self.metadata))

    # ---------- Pure updates (return new instance) ----------
    def rename(self, name: str) -> "Account":
        return replace(self, name=normalize_name(name))

    def with_primary_email(self, email: Optional[str]) -> "Account":
        return replace(self, primary_email=normalize_email(email))

    def with_primary_phone(self, phone: Optional[str]) -> "Account":
        return replace(self, primary_phone=normalize_phone(phone))

    def with_metadata(self, metadata: Optional[Mapping[str, Any]]) -> "Account":
        return replace(self, metadata=normalize_metadata(metadata))

    # ---------- Deterministic guards ----------
    def require_same_id(self, account_id: str) -> "Account":
        if normalize_id(account_id) != self.account_id:
            raise InvariantViolationError("account_id mismatch")
        return self
