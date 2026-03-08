# control_plane/governance/crm/crm_invariants.py
from typing import Any, Dict, Mapping, Optional

from core.errors import ValidationError

_MAX_ID_LEN = 80
_MAX_NAME_LEN = 200
_MAX_EMAIL_LEN = 254


def _normalize_str(value: str, *, field: str, max_len: int) -> str:
    if not isinstance(value, str):
        raise ValidationError(f"{field} must be a string")
    v = value.strip()
    if not v:
        raise ValidationError(f"{field} cannot be empty")
    if len(v) > max_len:
        raise ValidationError(f"{field} is too long")
    return v


def normalize_id(value: str) -> str:
    # IDs are caller-provided opaque strings (UUID, ULID, etc.)
    return _normalize_str(value, field="id", max_len=_MAX_ID_LEN)


def normalize_name(value: str) -> str:
    return _normalize_str(value, field="name", max_len=_MAX_NAME_LEN)


def normalize_email(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    v = _normalize_str(value, field="email", max_len=_MAX_EMAIL_LEN)
    # extremely small deterministic shape check (no costly RFC):
    if "@" not in v or "." not in v.split("@")[-1]:
        raise ValidationError("email is not syntactically valid")
    return v.lower()


def normalize_phone(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    # Keep permissive; just trim and ensure non-empty:
    v = value.strip()
    if not v:
        return None
    if len(v) > 40:
        raise ValidationError("phone is too long")
    return v


def normalize_metadata(meta: Optional[Mapping[str, Any]]) -> Dict[str, Any]:
    if meta is None:
        return {}
    if not isinstance(meta, Mapping):
        raise ValidationError("metadata must be a mapping")
    # shallow, deterministic copy with normalized keys
    out: Dict[str, Any] = {}
    for k, v in meta.items():
        if not isinstance(k, str):
            raise ValidationError("metadata keys must be strings")
        nk = k.strip()
        if not nk:
            raise ValidationError("metadata keys cannot be empty")
        out[nk] = v
    return out
