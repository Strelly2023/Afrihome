from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Mapping, Optional

from core.errors import ValidationError
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
    PURE: only normalization/validation; no generation, IO, or randomness.
    """

    name: str  # canonical provider name (lowercase, kebab/snake ok)
    version: Optional[str] = None  # optional logical version/variant

    def __post_init__(self) -> None:
        n = (self.name or "").strip().lower()
        if not n:
            raise ValidationError("provider name must be non-empty")
        object.__setattr__(self, "name", n)

        v = self.version
        if isinstance(v, str):
            v = v.strip() or None
        object.__setattr__(self, "version", v)


@dataclass(frozen=True, slots=True)
class ProviderConfig:
    """
    Immutable, non-sensitive configuration for a tenant's provider binding.

    Notes
    -----
    - Sensitive values MUST NOT appear here (no secret material).
    - Feature flags / plan entitlements MAY gate 'enabled' externally; this is a static snapshot.
    """

    provider: ProviderRef
    enabled: bool
    settings: Mapping[str, Any] = field(
        default_factory=dict
    )  # non-sensitive settings only (e.g., region, mode, endpoints)


@dataclass(frozen=True, slots=True)
class SecretRef:
    """
    Opaque reference to secret material managed by infra (e.g., vault/keystore/secret manager).
    This governance layer NEVER carries cleartext secret values.
    """

    id: str
    kind: str  # e.g., 'api_key', 'oauth_token', 'signing_secret'
    last_rotated_ms: Optional[UnixMillis] = None
    # Purely informational, safe preview (e.g., '****abcd'). Never expand here.
    redacted_preview: Optional[str] = None

    def __post_init__(self) -> None:
        sid = (self.id or "").strip()
        if not sid:
            raise ValidationError("secret id must be non-empty")
        object.__setattr__(self, "id", sid)

        k = (self.kind or "").strip().lower()
        if not k:
            raise ValidationError("secret kind must be non-empty")
        object.__setattr__(self, "kind", k)

        if self.redacted_preview is not None:
            rp = self.redacted_preview.strip()
            object.__setattr__(self, "redacted_preview", rp or None)


@dataclass(frozen=True, slots=True)
class ResolvedCredential:
    """
    Deterministic output of a credential resolution. NO cleartext material here.
    """

    provider: ProviderRef
    purpose: CredentialPurpose
    secret: SecretRef
    metadata: Mapping[str, Any] = field(
        default_factory=dict
    )  # non-sensitive tags (e.g., scopes, audience, sandbox flag)


@dataclass(frozen=True, slots=True)
class ProviderContext:
    """
    Immutable orchestration bundle returned by ProviderConfigService.
    Carries non-sensitive config and an opaque reference to secret material.
    """

    config: ProviderConfig
    credential: Optional[ResolvedCredential] = None
