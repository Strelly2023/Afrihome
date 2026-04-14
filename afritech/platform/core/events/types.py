from __future__ import annotations

"""
AfriTech Core Events â€” Event Types (GA-Sealed)

This module defines the canonical set of event type identifiers
used by the AfriTech platform.

Event types are:
- symbolic identifiers of facts
- stable over time
- independent of transport or infrastructure
- shared across all layers of the system

PURPOSE:
- Provide a common, authoritative event vocabulary
- Prevent ad-hoc or inconsistent event naming
- Enable deterministic replay and audit

RULES:
- Declarative definitions ONLY
- NO execution
- NO IO
- NO time
- NO publishing or routing logic
- Values MUST remain stable unless changed via ADR

Any change requires an ADR.
"""

from enum import Enum


# ============================================================================
# Canonical Event Types
# ============================================================================

class EventType(str, Enum):
    """
    Canonical AfriTech event type identifiers.

    Each value represents a factual occurrence within the system.
    Event types describe *what happened*, not *what to do*.

    These identifiers are consumed by:
    - audit systems
    - replay pipelines
    - analytics
    - external integrations

    They do NOT:
    - trigger behavior
    - encode workflows
    - imply ordering or causality
    """

    # ------------------------------------------------------------------
    # Authorization / Decision Events
    # ------------------------------------------------------------------

    AUTHORIZATION_DECIDED = "authorization.decided"

    # ------------------------------------------------------------------
    # Policy Events
    # ------------------------------------------------------------------

    POLICY_EVALUATED = "policy.evaluated"

    # ------------------------------------------------------------------
    # Quota Events
    # ------------------------------------------------------------------

    QUOTA_CONSUMED = "quota.consumed"
    QUOTA_EXHAUSTED = "quota.exhausted"

    # ------------------------------------------------------------------
    # Consent Events
    # ------------------------------------------------------------------

    CONSENT_EVALUATED = "consent.evaluated"
    CONSENT_GRANTED = "consent.granted"
    CONSENT_REVOKED = "consent.revoked"

    # ------------------------------------------------------------------
    # Risk Events
    # ------------------------------------------------------------------

    RISK_EVALUATED = "risk.evaluated"

    # ------------------------------------------------------------------
    # Identity Events
    # ------------------------------------------------------------------

    IDENTITY_CREATED = "identity.created"
    IDENTITY_DEACTIVATED = "identity.deactivated"

    # ------------------------------------------------------------------
    # Tenancy Events
    # ------------------------------------------------------------------

    TENANT_CREATED = "tenant.created"
    TENANT_SUSPENDED = "tenant.suspended"

    # ------------------------------------------------------------------
    # Finance / Payment Events
    # ------------------------------------------------------------------

    PAYMENT_PROCESSED = "payment.processed"

    # ------------------------------------------------------------------
    # Audit & Governance Events
    # ------------------------------------------------------------------

    AUDIT_RECORDED = "audit.recorded"

    # Operations
    OPERATION_STARTED = "operation.started"
    OPERATION_COMPLETED = "operation.completed"

    # Devices / IoT
    DEVICE_REGISTERED = "device.registered"
    DEVICE_DECOMMISSIONED = "device.decommissioned"

    # Data
    DATA_CREATED = "data.created"
    DATA_DELETED = "data.deleted"

    # Notifications
    NOTIFICATION_DISPATCHED = "notification.dispatched"
    NOTIFICATION_FAILED = "notification.failed"
