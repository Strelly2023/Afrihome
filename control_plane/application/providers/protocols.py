from typing import Optional, Protocol, runtime_checkable

from control_plane.application.execution.models import (
    CredentialPurpose,
    ProviderConfig,
    ProviderRef,
    ResolvedCredential,
)
from core.typing import TenantId


@runtime_checkable
class ProviderConfigRepository(Protocol):
    """
    Pure repository protocol to read provider config snapshots for a tenant.
    Infra implements this later (DB/kv/etc.). No IO in app layer.
    """

    def get(self, tenant_id: TenantId, provider: ProviderRef) -> Optional[ProviderConfig]: ...


@runtime_checkable
class CredentialResolver(Protocol):
    """
    Pure protocol interface that resolves credential *references* (NO cleartext).
    Concrete adapters live in infra and can call a secret manager.
    """

    def resolve(
        self,
        tenant_id: TenantId,
        provider: ProviderRef,
        purpose: CredentialPurpose,
    ) -> Optional[ResolvedCredential]: ...


@runtime_checkable
class ProviderPolicy(Protocol):
    """
    Pure policy hook to validate a provider context (config + resolved credential).
    Return (allowed, reason).
    Examples: blocklist providers, restrict sandbox in prod tenants, etc.
    """

    def evaluate(
        self,
        tenant_id: TenantId,
        context: ProviderConfig,
    ) -> tuple[bool, str]: ...
