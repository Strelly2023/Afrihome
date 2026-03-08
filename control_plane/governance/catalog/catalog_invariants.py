# control_plane/governance/catalog/catalo g_invariants.py
from typing import Any, Dict, Mapping, Optional

from core.errors import ValidationError

_MAX_ID_LEN = 80
_MAX_CODE_LEN = 80
_MAX_NAME_LEN = 200
_MAX_DESC_LEN = 2000


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
    # Opaque identifier: UUID/ULID/slug allowed
    return _normalize_str(value, field="id", max_len=_MAX_ID_LEN)


def normalize_code(value: str) -> str:
    # Product codes / tier codes: stable lowercase slugs (a-z0-9_-)
    v = _normalize_str(value, field="code", max_len=_MAX_CODE_LEN).lower()
    import re

    if not re.fullmatch(r"[a-z0-9][a-z0-9_\-]*", v):
        raise ValidationError("code must match [a-z0-9][a-z0-9_-]*")
    return v


def normalize_name(value: str) -> str:
    return _normalize_str(value, field="name", max_len=_MAX_NAME_LEN)


def normalize_desc(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    v = value.strip()
    if not v:
        return None
    if len(v) > _MAX_DESC_LEN:
        raise ValidationError("description is too long")
    return v


def normalize_metadata(meta: Optional[Mapping[str, Any]]) -> Dict[str, Any]:
    if meta is None:
        return {}
    if not isinstance(meta, Mapping):
        raise ValidationError("metadata must be a mapping")
    out: Dict[str, Any] = {}
    for k, v in meta.items():
        if not isinstance(k, str):
            raise ValidationError("metadata keys must be strings")
        nk = k.strip()
        if not nk:
            raise ValidationError("metadata keys cannot be empty")
        out[nk] = v
    return out
