from __future__ import annotations

"""
AfriTech Core Events â€” Domain Events (GA-Sealed)

This package contains domain-specific *facts* emitted by the AfriTech
platform. Domain events are immutable, declarative, and side-effect free.

They do NOT:
- execute logic
- enforce policy
- trigger workflows
- imply commands or intentions

Any change requires an ADR.
"""

# ============================================================================
# Authorization Domain Events
# ============================================================================

from afritech.platform.core.events.domain.authorization import AuthorizationDecided

# ============================================================================
# Policy Domain Events
# ============================================================================

from afritech.platform.core.events.domain.policy import PolicyEvaluated

# ============================================================================
# Quota Domain Events
# ============================================================================

from afritech.platform.core.events.domain.quota import QuotaConsumed, QuotaExhausted

# ============================================================================
# Risk Domain Events
# ============================================================================

from afritech.platform.core.events.domain.risk import RiskEvaluated

# ============================================================================
# Consent Domain Events
# ============================================================================

from afritech.platform.core.events.domain.consent import (
    ConsentEvaluated,
    ConsentGranted,
    ConsentRevoked,
)

# ============================================================================
# Identity Domain Events
# ============================================================================

from afritech.platform.core.events.domain.identity import (
    IdentityCreated,
    IdentityDeactivated,
)

# ============================================================================
# Tenancy Domain Events
# ============================================================================

from afritech.platform.core.events.domain.tenancy import (
    TenantCreated,
    TenantSuspended,
)

# ============================================================================
# Finance Domain Events
# ============================================================================

from afritech.platform.core.events.domain.finance import PaymentProcessed

# ============================================================================
# Audit Domain Events
# ============================================================================

from afritech.platform.core.events.domain.audit import AuditRecorded


# Operations
from afritech.platform.core.events.domain.operations import (
    OperationStarted,
    OperationCompleted,
)

# Device / IoT
from afritech.platform.core.events.domain.device import (
    DeviceRegistered,
    DeviceDecommissioned,
)

# Data
from afritech.platform.core.events.domain.data import (
    DataCreated,
    DataDeleted,
)

# Notifications
from afritech.platform.core.events.domain.notification import (
    NotificationDispatched,
    NotificationFailed,
)

# ============================================================================
# Frozen Public ABI
# ============================================================================

__all__ = [
    # Authorization
    "AuthorizationDecided",

    # Policy
    "PolicyEvaluated",

    # Quota
    "QuotaConsumed",
    "QuotaExhausted",

    # Risk
    "RiskEvaluated",

    # Consent
    "ConsentEvaluated",
    "ConsentGranted",
    "ConsentRevoked",

    # Identity
    "IdentityCreated",
    "IdentityDeactivated",

    # Tenancy
    "TenantCreated",
    "TenantSuspended",

    # Finance
    "PaymentProcessed",

    # Audit
    "AuditRecorded",

    # Operations
    "OperationStarted",
    "OperationCompleted",
    # Devices / IoT
    "DeviceRegistered",
    "DeviceDecommissioned",
    # Data
    "DataCreated",
    "DataDeleted",
    # Notifications
    "NotificationDispatched",
    "NotificationFailed",
    
]
