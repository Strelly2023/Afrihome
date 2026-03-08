from typing import Optional, Protocol, runtime_checkable

from core.rbac.policy_engine import Policy  # pure RBAC policy; deny-wins handled in engine
from core.typing import TenantId


@runtime_checkable
class PolicyProvider(Protocol):
    """
    Pure protocol that supplies a tenant-scoped RBAC Policy.
    NOTE: Phase 3 uses only interfaces; infra binds concrete providers later.
    """

    def policy_for(self, tenant_id: TenantId) -> Policy: ...


@runtime_checkable
class GovernancePolicy(Protocol):
    """
    Pure governance hook. Return a string reason to DENY, or None to allow evaluation to proceed.
    Examples (added later as needed): maintenance windows, kill switches, explicit blocklists.
    """

    def evaluate(self, *, tenant_id: TenantId, permission: str) -> Optional[str]: ...
