"""
GA Repository Protocol — Account
--------------------------------

Layer: Repositories (ports only, no IO)
Deterministic: YES
IO/ORM: NO

Notes
-----
• Accounts are tenant-scoped in the repository boundary.
• Implementations live in control_plane/infrastructure/* and must never leak infra types upward.
"""

from typing import Optional, Protocol, Tuple, runtime_checkable

from control_plane.governance.crm.account import Account
from control_plane.governance.tenants.tenant_id import TenantId


@runtime_checkable
class AccountRepository(Protocol):
    """
    Tenant-scoped repository contract for Accounts.

    Implementations MUST be deterministic and side-effect free from the caller's perspective.
    All external IO (DB, network, etc.) belongs to infrastructure adapters only.
    """

    # ----------- Read API (deterministic) -----------

    def get_by_id(self, tenant_id: TenantId, account_id: str) -> Optional[Account]:
        """
        Return the Account by id if present in the tenant scope; otherwise None.
        """
        ...

    def find_by_name(self, tenant_id: TenantId, name: str) -> Optional[Account]:
        """
        Case-insensitive, normalized name lookup in tenant scope.
        Returns the first stable match if multiple exist; None if not found.
        """
        ...

    def list_all(
        self,
        tenant_id: TenantId,
        *,
        limit: int = 200,
        offset: int = 0,
    ) -> Tuple[Account, ...]:
        """
        Return a stable, deterministic window of accounts for the tenant.
        Ordering is implementation-defined but MUST be stable across identical inputs.
        """
        ...

    # ----------- Write API (deterministic effects via infra) -----------

    def save(self, tenant_id: TenantId, account: Account) -> None:
        """
        Upsert semantics in tenant scope (idempotent).
        Must be strictly deterministic given identical inputs.
        """
        ...

    def delete(self, tenant_id: TenantId, account_id: str) -> None:
        """
        Delete by id in tenant scope.
        Non-existent ids MUST be treated as a no-op (idempotent delete).
        """
        ...
