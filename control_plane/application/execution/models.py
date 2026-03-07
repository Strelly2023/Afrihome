#control_plane/application/execution/models.py
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Mapping, Optional, Tuple
from core.execution import ExecutionContext
from core.typing import (
    TenantId, UserId, RequestId, CorrelationId, CausationId, UnixMillis, RoleName
)

class ActorKind(Enum):
    USER = auto()
    API_KEY = auto()
    SYSTEM = auto()
    OPERATOR = auto()

@dataclass(frozen=True, slots=True)
class Actor:
    """
    Pure, immutable actor snapshot (no RBAC resolution here).
    """
    kind: ActorKind
    user_id: Optional[UserId] = None
    roles: Tuple[RoleName, ...] = ()
    principal: Optional[str] = None  # opaque identifier (e.g., api key id, service name)

@dataclass(frozen=True, slots=True)
class ExecutionFrame:
    """
    Immutable application-level frame for a single request.
    Carries:
      - ExecutionContext (core) for time/uuid discipline and write-mode boundaries
      - Tenant identity (id + slug) for isolation
      - Actor surface (no RBAC decisions yet)
      - Opaque feature snapshot (pure governance value)
      - Normalized inbound headers (read-only)
    """
    ctx: ExecutionContext

    request_id: RequestId
    correlation_id: CorrelationId
    causation_id: CausationId
    timestamp_ms: UnixMillis

    tenant_id: TenantId
    tenant_slug: str

    actor: Actor

    feature_snapshot: Any
    headers: Mapping[str, str]