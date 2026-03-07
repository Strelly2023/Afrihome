from dataclasses import dataclass

from core.identity.uuid import UUIDProvider
from core.typing import TenantId as CoreTenantId, AggregateId


@dataclass(frozen=True, slots=True)
class TenantId:
    """
    Strong platform-level TenantId.

    - Plain string wrapper (immutable)
    - Compatible with core.typing.TenantId
    - Optional deterministic factory using UUIDProvider
    """
    value: str

    def __post_init__(self) -> None:
        if not isinstance(self.value, str) or not self.value.strip():
            raise ValueError("TenantId must be a non-empty string")

    def __str__(self) -> str:
        return self.value

    # ---------- Adapters to/from core ----------

    def to_core(self) -> CoreTenantId:
        return CoreTenantId(self.value)

    @staticmethod
    def from_core(cid: CoreTenantId) -> "TenantId":
        return TenantId(str(cid))

    # ---------- Deterministic factory (optional) ----------

    @staticmethod
    def new(uuid_provider: UUIDProvider) -> "TenantId":
        """
        Deterministically derive a new TenantId from the injected UUID provider.
        Governance remains infra-free; UUIDProvider comes from core.
        """
        agg: AggregateId = uuid_provider.new_aggregate_id()
        return TenantId(str(agg))