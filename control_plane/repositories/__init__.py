# control_plane/repositories/__init__.py
"""
AfriHome — Repository Protocols (IO-free)
Layer order: governance → repositories → application → api → infrastructure
This package exposes PURE Protocols only. No implementations, no IO.
"""

# from .rbac_state_repository import RbacStateRepository, RBACStateRepository
from .apikey_repository import ApiKeyRepository

# from .audit_repository import AuditWriter, AuditReader
from .event_repository import EventTypeRegistry
from .feature_repository import FeatureRepository
from .identity_repository import IdentityRepository
from .notification_repository import NotificationRepository
from .plan_repository import PlanRepository
from .provider_config_repository import ProviderConfigRepository
from .provider_repository import ProviderRepository
from .rbac_state_repository import RBACStateRepository, RbacStateRepository  # Back-compat alias
from .role_repository import RoleRepository
from .subscription_repository import SubscriptionRepository
from .tenant_repository import TenantRepository
from .usage_aggregate_repository import UsageAggregateRepository
from .usage_counter_repository import UsageCounterRepository
from .usage_repository import UsageRepository
from .webhook_verification_repository import WebhookVerificationRepository

# Unified audit repository (append/read) — present today
try:
    from .audit_repository import AuditRepository  # noqa: F401
except Exception:
    # Keep imports soft to avoid masking unrelated test import issues
    pass


__all__ = [
    "AuditRepository",
    "TenantRepository",
    "IdentityRepository",
    "RoleRepository",
    "PlanRepository",
    "SubscriptionRepository",
    "FeatureRepository",
    "UsageRepository",
    "UsageCounterRepository",
    "UsageAggregateRepository",
    "NotificationRepository",
    "ProviderRepository",
    "ProviderConfigRepository",
    "ApiKeyRepository",
    "RBACStateRepository",
    "RbacStateRepository",
    "AuditWriter",
    "AuditReader",
    "EventTypeRegistry",
    "WebhookVerificationRepository",
]
