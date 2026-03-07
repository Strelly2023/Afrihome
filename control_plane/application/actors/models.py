#control_plane/application/actors/models.py
from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional, Tuple
from core.typing import UserId, RoleName
# Pure, immutable, and deterministic data shapes — consistent with core style.  # noqa
# (No IO, no side effects.)                                                     # noqa

class ActorKind(Enum):
    USER = auto()
    API_KEY = auto()
    SYSTEM = auto()
    OPERATOR = auto()

@dataclass(frozen=True, slots=True)
class Actor:
    """
    Immutable actor surface used across application services.
    NOTE: No RBAC decisioning lives here; this module only maps inputs to identity.
    """
    kind: ActorKind
    user_id: Optional[UserId] = None
    roles: Tuple[RoleName, ...] = ()
    principal: Optional[str] = None  # opaque (e.g., api key id, service name)