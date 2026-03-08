"""
GA Repository Protocol — Product (Catalog)
------------------------------------------

Layer: Repositories (ports only; no IO)
Deterministic: YES
IO/ORM: NO

Purpose
-------
A tenant-scoped repository contract for Catalog Products.
Used by: plans, subscriptions, and billing alignment.

Notes
-----
• Implementations live in control_plane/infrastructure/* and must not leak infra types upward.
• All methods must be deterministic for identical inputs.
• Deletions are idempotent (no-op if entity is missing).
"""

from typing import Optional, Protocol, Tuple, runtime_checkable

from control_plane.governance.catalog.product import Product
from control_plane.governance.catalog.product_id import ProductId
from control_plane.governance.tenants.tenant_id import TenantId


@runtime_checkable
class ProductRepository(Protocol):
    """
    Tenant-scoped repository contract for Catalog Products.

    Implementations MUST:
      • be deterministic (stable ordering for identical inputs),
      • avoid side effects beyond persistence,
      • never raise on 'not found'—return None or empty tuples,
      • treat delete of a missing id as a no-op (idempotent).
    """

    # ---------- Read (deterministic) ----------

    def get_by_id(self, tenant_id: TenantId, product_id: ProductId) -> Optional[Product]:
        """
        Return Product by id if present in tenant scope; otherwise None.
        """
        ...

    def find_by_name(self, tenant_id: TenantId, name: str) -> Optional[Product]:
        """
        Case-insensitive, normalized name lookup within tenant scope.
        If multiple matches exist, return a stable first match.
        """
        ...

    def find_by_code(self, tenant_id: TenantId, code: str) -> Optional[Product]:
        """
        Look up by canonical product code if you model one in metadata or naming conventions.
        Optional—implementations may map code -> name or dedicated field; return None if unsupported.
        """
        ...

    def list_all(
        self,
        tenant_id: TenantId,
        *,
        limit: int = 200,
        offset: int = 0,
    ) -> Tuple[Product, ...]:
        """
        Return a stable, deterministic window of products.
        Ordering is implementation-defined but MUST be stable across identical inputs.
        """
        ...

    # ---------- Write (deterministic effects via infra adapters) ----------

    def save(self, tenant_id: TenantId, product: Product) -> None:
        """
        Upsert semantics in tenant scope (idempotent).
        Saving the same Product twice MUST be a no-op.
        """
        ...

    def delete(self, tenant_id: TenantId, product_id: ProductId) -> None:
        """
        Delete by id in tenant scope.
        Non-existent ids MUST be treated as a no-op (idempotent delete).
        """
        ...
