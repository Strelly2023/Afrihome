# control_plane/governance/catalog/__init__.py
"""
GA Governance — Catalog (pure aggregates)
-----------------------------------------

LAYER: Governance (pure)
Deterministic: YES
IO/ORM: NO

Used by: plans, subscriptions, billing alignment
"""

__all__ = [
    "ProductId",
    "ProductTier",
    "ServiceDefinition",
    "Product",
]
