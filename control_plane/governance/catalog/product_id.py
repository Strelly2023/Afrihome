# control_plane/governance/catalog/product_id.py
from dataclasses import dataclass

from .catalog_invariants import normalize_id


@dataclass(frozen=True)
class ProductId:
    value: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "value", normalize_id(self.value))

    def __str__(self) -> str:
        return self.value
