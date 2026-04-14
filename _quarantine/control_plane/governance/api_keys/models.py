# control_plane/governance/api_keys/models.py
from dataclasses import dataclass
from typing import Optional, Tuple
from core.typing import TenantId

@dataclass(frozen=True, slots=True)
class ApiKeyId:
    value: str  # deterministic id (not the secret token)

@dataclass(frozen=True, slots=True)
class ApiKeyScope:
    patterns: Tuple[str, ...] = ()     # permission patterns (deny-wins handled later)

@dataclass(frozen=True, slots=True)
class ApiKey:
    tenant_id: TenantId
    key_id: ApiKeyId
    name: str
    scopes: ApiKeyScope
    enabled: bool = True

@dataclass(frozen=True, slots=True)
class ApiKeyPolicy:
    # allow/deny rules at governance level
    allow_service_accounts: bool = True