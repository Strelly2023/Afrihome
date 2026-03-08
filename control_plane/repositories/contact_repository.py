"""
GA Repository Protocol — Contact
--------------------------------

Layer: Repositories (ports only, no IO)
Deterministic: YES
IO/ORM: NO

Notes
-----
• Contacts belong to an Account and are tenant-scoped at the repository boundary.
• Implementations live in control_plane/infrastructure/* and must never leak infra types upward.
"""

from typing import Optional, Protocol, Tuple, runtime_checkable

from control_plane.governance.crm.contact import Contact
from control_plane.governance.tenants.tenant_id import TenantId


@runtime_checkable
class ContactRepository(Protocol):
    """
    Tenant-scoped repository contract for Contacts.

    Implementations MUST be deterministic and side-effect free from the caller's perspective.
    All external IO (DB, network, etc.) belongs to infrastructure adapters only.
    """

    # ----------- Read API (deterministic) -----------

    def get_by_id(self, tenant_id: TenantId, contact_id: str) -> Optional[Contact]:
        """
        Return the Contact by id if present in the tenant scope; otherwise None.
        """
        ...

    def list_by_account(
        self,
        tenant_id: TenantId,
        account_id: str,
        *,
        limit: int = 200,
        offset: int = 0,
    ) -> Tuple[Contact, ...]:
        """
        Return a stable, deterministic window of contacts for the given account in tenant scope.
        Ordering is implementation-defined but MUST be stable across identical inputs.
        """
        ...

    def find_by_email(
        self,
        tenant_id: TenantId,
        account_id: str,
        email: str,
    ) -> Optional[Contact]:
        """
        Return the Contact matching email (normalized) within the account, or None.
        """
        ...

    # ----------- Write API (deterministic effects via infra) -----------

    def save(self, tenant_id: TenantId, contact: Contact) -> None:
        """
        Upsert semantics in tenant/account scope (idempotent).
        Must be strictly deterministic given identical inputs.
        """
        ...

    def delete(self, tenant_id: TenantId, contact_id: str) -> None:
        """
        Delete by id in tenant scope.
        Non-existent ids MUST be treated as a no-op (idempotent delete).
        """
        ...
