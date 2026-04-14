#control_plane/application/execution/actor_resolution.py

from typing import Mapping, Optional, Tuple
from control_plane.application.actors.service import ActorService
from core.typing import UserId, RoleName
from core.kernel.invariants import assert_not_none
from core.errors import ValidationError
from .models import Actor, ActorKind
from .constants import HDR_ACTOR_KIND, HDR_USER_ID, HDR_ROLES, HDR_PRINCIPAL

_VALID = {
    "user": ActorKind.USER,
    "api_key": ActorKind.API_KEY,
    "system": ActorKind.SYSTEM,
    "operator": ActorKind.OPERATOR,
}

def _parse_roles(s: Optional[str]) -> Tuple[RoleName, ...]:
    if not s:
        return ()
    items = [r.strip() for r in s.split(",") if r.strip()]
    return tuple(RoleName(r) for r in items)

def map_headers_to_actor(headers: Mapping[str, str]) -> Actor:
    """
    Deterministic header -> Actor mapping (no RBAC decisions here).
    """
    assert_not_none(headers, "headers")

    kind_raw = (headers.get(HDR_ACTOR_KIND) or "").strip().lower()
    if kind_raw not in _VALID:
        raise ValidationError("x-actor-kind must be one of: USER, API_KEY, SYSTEM, OPERATOR")

    kind = _VALID[kind_raw]
    principal = (headers.get(HDR_PRINCIPAL) or "").strip() or None
    roles = _parse_roles(headers.get(HDR_ROLES))

    if kind is ActorKind.USER:
        uid_raw = (headers.get(HDR_USER_ID) or "").strip()
        if not uid_raw:
            raise ValidationError("x-user-id required for USER actor")
        return Actor(kind=ActorKind.USER, user_id=UserId(uid_raw), roles=roles, principal=principal)

    # Non-USER kinds MUST NOT carry a user_id at this stage.
    return Actor(kind=kind, user_id=None, roles=roles, principal=principal)


def map_headers_to_actor(headers: dict[str, str]):
    return ActorService.from_headers(headers)
