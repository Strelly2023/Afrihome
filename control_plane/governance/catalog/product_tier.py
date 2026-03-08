# control_plane/governance/catalog/product_tier.py
from dataclasses import dataclass
from typing import Any, Dict, Optional

from .catalog_invariants import normalize_code, normalize_desc, normalize_metadata, normalize_name


@dataclass(frozen=True)
class ProductTier:
    """
    A catalog tier (e.g., free, standard, pro).
    """

    code: str
    name: str
    description: Optional[str]
    metadata: Dict[str, Any]

    def __post_init__(self) -> None:
        object.__setattr__(self, "code", normalize_code(self.code))
        object.__setattr__(self, "name", normalize_name(self.name))
        object.__setattr__(self, "description", normalize_desc(self.description))
        object.__setattr__(self, "metadata", normalize_metadata(self.metadata))

    # No mutation; add helpers if needed (e.g., rename) in Product aggregate.
