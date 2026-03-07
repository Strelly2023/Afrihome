"""
AfriHome Control Plane — Application/Providers
PHASE: 3.11 (Orchestration only)
IO: NONE | Threads/async: NONE | Deterministic: YES

Exports:
- ProviderRef, ProviderConfig, SecretRef, ResolvedCredential, ProviderContext, CredentialPurpose
- ProviderConfigRepository, CredentialResolver, ProviderPolicy
- ProviderConfigService
"""
from .models import (
    ProviderRef,
    ProviderConfig,
    SecretRef,
    ResolvedCredential,
    ProviderContext,
    CredentialPurpose,
)
from .protocols import (
    ProviderConfigRepository,
    CredentialResolver,
    ProviderPolicy,
)
from .service import ProviderConfigService

__all__ = [
    "ProviderRef", "ProviderConfig", "SecretRef", "ResolvedCredential",
    "ProviderContext", "CredentialPurpose",
    "ProviderConfigRepository", "CredentialResolver", "ProviderPolicy",
    "ProviderConfigService",
]
