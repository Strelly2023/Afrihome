# control_plane/governance/crm/lead.py
from dataclasses import dataclass, replace
from typing import Any, Dict, Mapping, Optional

from .crm_invariants import (
    normalize_email,
    normalize_id,
    normalize_metadata,
    normalize_name,
    normalize_phone,
)


@dataclass(frozen=True)
class Lead:
    """
    Inbound prospect (pre-account), kept pure for deterministic pipelines.
    """

    lead_id: str
    display_name: str
    email: Optional[str]
    phone: Optional[str]
    source: Optional[str]
    metadata: Dict[str, Any]

    def __post_init__(self) -> None:
        object.__setattr__(self, "lead_id", normalize_id(self.lead_id))
        object.__setattr__(self, "display_name", normalize_name(self.display_name))
        object.__setattr__(self, "email", normalize_email(self.email))
        object.__setattr__(self, "phone", normalize_phone(self.phone))
        object.__setattr__(self, "source", self._normalize_source(self.source))
        object.__setattr__(self, "metadata", normalize_metadata(self.metadata))

    @staticmethod
    def _normalize_source(src: Optional[str]) -> Optional[str]:
        if src is None:
            return None
        s = src.strip()
        if not s:
            return None
        if len(s) > 100:
            from core.errors import ValidationError

            raise ValidationError("source is too long")
        return s.lower()

    def rename(self, display_name: str) -> "Lead":
        return replace(self, display_name=normalize_name(display_name))

    def with_email(self, email: Optional[str]) -> "Lead":
        return replace(self, email=normalize_email(email))

    def with_phone(self, phone: Optional[str]) -> "Lead":
        return replace(self, phone=normalize_phone(phone))

    def with_source(self, source: Optional[str]) -> "Lead":
        return replace(self, source=self._normalize_source(source))

    def with_metadata(self, metadata: Optional[Mapping[str, Any]]) -> "Lead":
        return replace(self, metadata=normalize_metadata(metadata))
