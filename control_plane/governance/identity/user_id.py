from dataclasses import dataclass

from core.identity.uuid import UUIDProvider
from core.typing import UserId as CoreUserId, AggregateId


@dataclass(frozen=True, slots=True)
class UserId:
    """
    Strong platform-level UserId.

    - String wrapper (immutable)
    - Compatible with core.typing.UserId
    - Deterministic factory (uses injected UUIDProvider)
    """
    value: str

    def __post_init__(self) -> None:
        if not isinstance(self.value, str) or not self.value.strip():
            raise ValueError("UserId must be a non-empty string")

    def __str__(self) -> str:
        return self.value

    def to_core(self) -> CoreUserId:
        return CoreUserId(self.value)

    @staticmethod
    def from_core(cid: CoreUserId) -> "UserId":
        return UserId(str(cid))

    @staticmethod
    def new(uuid_provider: UUIDProvider) -> "UserId":
        agg: AggregateId = uuid_provider.new_aggregate_id()
        return UserId(str(agg))