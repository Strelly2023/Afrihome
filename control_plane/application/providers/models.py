from dataclasses import dataclass
from enum import Enum, auto
from typing import Mapping, Any, Optional
from core.typing import UnixMillis

class CredentialPurpose(Enum):
    """
    Logical purpose for a credential resolution; used to pick a specific material set.
    Examples: 'default', 'inbound_webhook', 'outbound_api', 'sandbox'.
    """
    DEFAULT = auto()
    INBOUND_WEBHOOK = auto()
    OUTBOUND_API = auto()
    SANDBOX = auto()

@dataclass(frozen=True, slots=True)
class ProviderRef:
    """
    Opaque reference to a provider for a tenant (e.g., 'stripe', 'sendgrid', 'twilio').
    """
    name: str            # canonical provider name (lowercase, kebab/snake ok)
    version: Optional[str] = None   # optional logical version/variant

@dataclass(frozen=True, slots=True)
class ProviderConfig:
    """
    Immutable, non-sensitive configuration for a tenant's provider binding.
    NOTE:
      - Sensitive values MUST NOT appear here (no secrets).
      - Feature flags / plan entitlements MAY gate 'enabled' externally; this is a static snapshot.
    """
    provider: ProviderRef
    enabled: bool
    settings: Mapping[str, Any] = ()   # non-sensitive settings only (e.g., region, mode, endpoints)

@dataclass(frozen=True, slots=True)
class SecretRef:
    """
    Opaque reference to secret material managed by infra (e.g., vault/keystore/secret manager).
    This application layer NEVER carries cleartext secrets.
    """
    id: str
    kind: str                          # e.g., 'api_key', 'oauth_token', 'signing_secret'
    last_rotated_ms: Optional[UnixMillis] = None
    redacted_preview: Optional[str] = None  # e.g., '****abcd' (purely informational)

@dataclass(frozen=True, slots=True)
class ResolvedCredential:
    """
    Deterministic output of a credential resolution. NO cleartext material here.
    """
    provider: ProviderRef
    purpose: CredentialPurpose
    secret: SecretRef
    metadata: Mapping[str, Any] = ()   # non-sensitive tags (e.g., scopes, audience, sandbox flag)

@dataclass(frozen=True, slots=True)
class ProviderContext:
    """
    Immutable orchestration bundle returned by ProviderConfigService.
    Carries non-sensitive config and an opaque reference to secret material.
    """
    config: ProviderConfig
    credential: Optional[ResolvedCredential] = None