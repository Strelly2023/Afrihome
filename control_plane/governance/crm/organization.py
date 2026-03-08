# control_plane/governance/crm/organization.py
from dataclasses import dataclass, replace
from typing import Any, Dict, Mapping, Optional

from .crm_invariants import normalize_id, normalize_metadata, normalize_name


@dataclass(frozen=True)
class Organization:
    """
    A logical org/department node under an Account.
    """

    organization_id: str
    account_id: str
    name: str
    parent_org_id: Optional[str]
    metadata: Dict[str, Any]

    def __post_init__(self) -> None:
        object.__setattr__(self, "organization_id", normalize_id(self.organization_id))
        object.__setattr__(self, "account_id", normalize_id(self.account_id))
        object.__setattr__(self, "name", normalize_name(self.name))
        object.__setattr__(
            self, "parent_org_id", normalize_id(self.parent_org_id) if self.parent_org_id else None
        )
        object.__setattr__(self, "metadata", normalize_metadata(self.metadata))

    def rename(self, name: str) -> "Organization":
        return replace(self, name=normalize_name(name))

    def reparent(self, parent_org_id: Optional[str]) -> "Organization":
        pid = normalize_id(parent_org_id) if parent_org_id else None
        # Optional: prevent self-parenting deterministically (no IO needed)
        if pid and pid == self.organization_id:
            raise ValueError("organization cannot parent itself")
        return replace(self, parent_org_id=pid)

    def with_metadata(self, metadata: Optional[Mapping[str, Any]]) -> "Organization":
        return replace(self, metadata=normalize_metadata(metadata))
