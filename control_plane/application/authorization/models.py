from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional, Tuple

from core.typing import RoleName


class DecisionStage(Enum):
    """
    Composite decision pipeline stages.
    GOVERNANCE -> RBAC -> DEFAULT_DENY
    """

    GOVERNANCE = auto()
    RBAC = auto()
    DEFAULT_DENY = auto()


@dataclass(frozen=True, slots=True)
class AccessDecision:
    """
    Immutable access decision used by application services.
    """

    allowed: bool
    stage: DecisionStage
    reason: str
    role: Optional[RoleName] = None  # role that matched (if any)
    pattern: Optional[str] = None  # permission pattern that matched (if any)
    # Optional debugging sugar (safe to expose in operator/admin views)
    evaluated_roles: Tuple[RoleName, ...] = ()
    permission: Optional[str] = None
