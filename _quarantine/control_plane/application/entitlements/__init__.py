"""
AfriHome Control Plane — Application/Entitlements
PHASE: 3.5 (Orchestration only)
IO: NONE | Threads/async: NONE | Deterministic: YES

Exports:
- EntitlementDecision
- QuotaDecision, QuotaExceededError
- QuotaPolicy, WindowKind
- EntitlementProvider, QuotaPolicyProvider, UsageReader, WindowCalculator
- EntitlementsService, QuotaService
"""
from .models import EntitlementDecision, QuotaDecision, QuotaExceededError
from .protocols import (
    EntitlementProvider,
    QuotaPolicyProvider,
    UsageReader,
    WindowCalculator,
    QuotaPolicy,
    WindowKind,
)
from .service import EntitlementsService, QuotaService

__all__ = [
    # results
    "EntitlementDecision", "QuotaDecision", "QuotaExceededError",
    # policy types
    "QuotaPolicy", "WindowKind",
    # protocols
    "EntitlementProvider", "QuotaPolicyProvider", "UsageReader", "WindowCalculator",
    # services
    "EntitlementsService", "QuotaService",
]