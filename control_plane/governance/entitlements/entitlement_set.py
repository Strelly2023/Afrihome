# control_plane/governance/entitlements/entitlement_set.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable

from .entitlement import Entitlement


@dataclass(frozen=True)
class EntitlementSet:
    """
    A deterministic, pure collection of entitlements derived from:
      - Plan + PlanFeatures
      - Feature flags / rules
      - Subscription state / overrides
    """

    items: Dict[str, Entitlement]  # key -> Entitlement

    # ---------- Queries ----------

    def has(self, key: str) -> bool:
        k = key.strip().lower()
        return k in self.items

    def get(self, key: str) -> Entitlement | None:
        k = key.strip().lower()
        return self.items.get(k)

    # ---------- Composition (pure) ----------

    def merge_overrides(self, overrides: Iterable[Entitlement]) -> "EntitlementSet":
        """
        Apply overrides deterministically (replace by key), returning a NEW set.
        """
        merged = dict(self.items)
        for ent in overrides:
            merged[ent.key] = ent
        return EntitlementSet(merged)
