"""
AfriHome Control Plane — Governance · Integrations (Phase 1.9)

Pure governance models for 3rd-party integrations:
- ProviderConfig        : immutable provider registry entries (no secrets here)
- WebhookVerification   : immutable webhook verification policy (no crypto here)

Notes:
- Secrets are referenced via opaque IDs (e.g., "secret://providers/stripe/webhook").
- Application layer will fetch secrets and perform verification.
- Infrastructure layer will handle HTTP, crypto, retries, and persistence.
"""

from .provider_config import (
    ProviderConfig,
    ProviderKind,
    normalize_namespace_key,
    normalize_provider_key,
)
from .webhook_verification import (
    HttpMethod,
    SignatureAlgorithm,
    WebhookVerification,
    normalize_header_name,
    normalize_path,
)

__all__ = [
    "ProviderKind",
    "normalize_provider_key",
    "normalize_namespace_key",
    "ProviderConfig",
    "HttpMethod",
    "SignatureAlgorithm",
    "normalize_header_name",
    "normalize_path",
    "WebhookVerification",
]
