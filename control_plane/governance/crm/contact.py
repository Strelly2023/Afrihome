# control_plane/governance/crm/contact.py
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
class Contact:
    """
    A person record attached to an Account/Organization (pure).
    """

    contact_id: str
    account_id: str
    full_name: str
    email: Optional[str]
    phone: Optional[str]
    metadata: Dict[str, Any]

    def __post_init__(self) -> None:
        object.__setattr__(self, "contact_id", normalize_id(self.contact_id))
        object.__setattr__(self, "account_id", normalize_id(self.account_id))
        object.__setattr__(self, "full_name", normalize_name(self.full_name))
        object.__setattr__(self, "email", normalize_email(self.email))
        object.__setattr__(self, "phone", normalize_phone(self.phone))
        object.__setattr__(self, "metadata", normalize_metadata(self.metadata))

    def rename(self, full_name: str) -> "Contact":
        return replace(self, full_name=normalize_name(full_name))

    def with_email(self, email: Optional[str]) -> "Contact":
        return replace(self, email=normalize_email(email))

    def with_phone(self, phone: Optional[str]) -> "Contact":
        return replace(self, phone=normalize_phone(phone))

    def with_metadata(self, metadata: Optional[Mapping[str, Any]]) -> "Contact":
        return replace(self, metadata=normalize_metadata(metadata))

    def require_same_account(self, account_id: str) -> "Contact":
        if normalize_id(account_id) != self.account_id:
            raise InvariantViolationError("contact not attached to given account_id")
        return self
