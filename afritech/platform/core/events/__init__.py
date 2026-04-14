from __future__ import annotations

"""
AfriTech Core Events (GA-Sealed)

This package defines the declarative event language of the AfriTech
platform. It specifies what *facts* may be represented as events,
independent of transport, persistence, or execution.

The events layer is:
- Pure
- Immutable
- Deterministic
- Authority-safe

PURPOSE:
- Establish a canonical event vocabulary
- Enable deterministic audit and replay
- Provide a stable semantic boundary for infrastructure

RULES:
- Declarative exports ONLY
- NO execution
- NO IO
- NO time generation
- Public ABI MUST be explicit

Any change requires an ADR.
"""

# ============================================================================
# Base Event Primitives
# ============================================================================

from afritech.platform.core.events.base import (
    DomainEvent,
)

from afritech.platform.core.events.headers import (
    EventHeaders,
)

from afritech.platform.core.events.envelope import (
    EventEnvelope,
)

# ============================================================================
# Event Type Vocabulary
# ============================================================================

from afritech.platform.core.events.types import (
    EventType,
)

# ============================================================================
# Authorization Domain Events
# ============================================================================

from afritech.platform.core.events.domain.authorization import (
    AuthorizationDecided,
)

# ============================================================================
# Policy Domain Events
# ============================================================================

from afritech.platform.core.events.domain.policy import (
    PolicyEvaluated,
)

# ============================================================================
# Quota Domain Events
# ============================================================================

from afritech.platform.core.events.domain.quota import (
    QuotaConsumed,
    QuotaExhausted,
)

# ============================================================================
# Risk Domain Events
# ============================================================================

from afritech.platform.core.events.domain.risk import (
    RiskEvaluated,
)

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
# Finance / Payment Domain Events
# ============================================================================

from afritech.platform.core.events.domain.finance import (
    PaymentProcessed,
)

# ============================================================================
# Audit Domain Events
# ============================================================================

from afritech.platform.core.events.domain.audit import (
    AuditRecorded,
)
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
    # Base primitives
    "DomainEvent",
    "EventHeaders",
    "EventEnvelope",

    # Event vocabulary
    "EventType",

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
