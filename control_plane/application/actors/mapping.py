# control_plane/application/actors/mapping.py
from typing import Mapping, Optional, Tuple

from core.errors import ValidationError
from core.kernel.invariants import assert_not_none
from core.typing import RoleName, UserId

from .constants import HDR_ACTOR_KIND, HDR_PRINCIPAL, HDR_ROLES, HDR_USER_ID
from .models import Actor, ActorKind

_VALID_KINDS = {
    "user": ActorKind.USER,
    "api_key": ActorKind.API_KEY,
    "system": ActorKind.SYSTEM,
    "operator": ActorKind.OPERATOR,
}


def _parse_roles(raw: Optional[str]) -> Tuple[RoleName, ...]:
    if not raw:
        return ()
    items = [r.strip() for r in raw.split(",") if r.strip()]
    # Keep insertion order, remove duplicates deterministically.
    seen = set()
    out = []
    for r in items:
        if r not in seen:
            seen.add(r)
            out.append(RoleName(r))
    return tuple(out)


def map_headers_to_actor(headers: Mapping[str, str]) -> Actor:
    """
    Pure mapping: normalized headers -> Actor snapshot.
    No RBAC, no IO, no persistence.
    """
    assert_not_none(headers, "headers")

    kind_raw = (headers.get(HDR_ACTOR_KIND) or "").strip().lower()
    if kind_raw not in _VALID_KINDS:
        raise ValidationError("x-actor-kind must be one of: USER, API_KEY, SYSTEM, OPERATOR")

    kind = _VALID_KINDS[kind_raw]
    principal = (headers.get(HDR_PRINCIPAL) or "").strip() or None
    roles = _parse_roles(headers.get(HDR_ROLES))

    if kind is ActorKind.USER:
        uid_raw = (headers.get(HDR_USER_ID) or "").strip()
        if not uid_raw:
            raise ValidationError("x-user-id required for USER actor")
        return Actor(kind=ActorKind.USER, user_id=UserId(uid_raw), roles=roles, principal=principal)

    # Non-USER kinds must not carry user_id at this stage.
    return Actor(kind=kind, user_id=None, roles=roles, principal=principal)
