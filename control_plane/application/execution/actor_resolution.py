# control_plane/application/execution/actor_resolution.py

from typing import Optional, Tuple

from control_plane.application.actors.service import ActorService
from core.typing import RoleName

from .models import ActorKind

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


def map_headers_to_actor(headers: dict[str, str]):
    return ActorService.from_headers(headers)
