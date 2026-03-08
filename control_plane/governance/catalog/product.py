# control_plane/governance/catalog/product.py
from dataclasses import dataclass, replace
from typing import Any, Dict, Mapping, Optional, Tuple

from core.errors import ValidationError

from .catalog_invariants import (
    normalize_desc,
    normalize_metadata,
    normalize_name,
)
from .product_id import ProductId
from .product_tier import ProductTier
from .service_definition import ServiceDefinition


@dataclass(frozen=True)
class Product:
    """
    A catalog Product: stable identity + tiers + service definitions.
    Pure and deterministic. No IO, no ORM.
    """

    product_id: ProductId
    name: str
    description: Optional[str]
    tiers: Tuple[ProductTier, ...]
    services: Tuple[ServiceDefinition, ...]
    metadata: Dict[str, Any]

    def __post_init__(self) -> None:
        # product_id validated by ProductId
        object.__setattr__(self, "name", normalize_name(self.name))
        object.__setattr__(self, "description", normalize_desc(self.description))
        # Validate tier/service uniqueness & stable ordering guarantees
        unique_tier_codes = set()
        for t in self.tiers:
            if t.code in unique_tier_codes:
                raise ValidationError(f"duplicate tier code: {t.code!r}")
            unique_tier_codes.add(t.code)

        unique_service_codes = set()
        for s in self.services:
            if s.code in unique_service_codes:
                raise ValidationError(f"duplicate service code: {s.code!r}")
            unique_service_codes.add(s.code)

        object.__setattr__(self, "metadata", normalize_metadata(self.metadata))

    # --------- Pure updates (return a new instance) ---------

    def rename(self, name: str) -> "Product":
        return replace(self, name=normalize_name(name))

    def with_description(self, description: Optional[str]) -> "Product":
        return replace(self, description=normalize_desc(description))

    def with_metadata(self, metadata: Optional[Mapping[str, Any]]) -> "Product":
        return replace(self, metadata=normalize_metadata(metadata))

    def add_tier(self, tier: ProductTier) -> "Product":
        if any(t.code == tier.code for t in self.tiers):
            raise ValidationError(f"tier already exists: {tier.code!r}")
        return replace(self, tiers=self.tiers + (tier,))

    def remove_tier(self, code: str) -> "Product":
        code = code.strip().lower()
        if not any(t.code == code for t in self.tiers):
            return self  # idempotent no-op
        return replace(self, tiers=tuple(t for t in self.tiers if t.code != code))

    def add_service(self, svc: ServiceDefinition) -> "Product":
        if any(s.code == svc.code for s in self.services):
            raise ValidationError(f"service already exists: {svc.code!r}")
        return replace(self, services=self.services + (svc,))

    def remove_service(self, code: str) -> "Product":
        code = code.strip().lower()
        if not any(s.code == code for s in self.services):
            return self  # idempotent no-op
        return replace(self, services=tuple(s for s in self.services if s.code != code))
