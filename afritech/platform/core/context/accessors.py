from __future__ import annotations

"""
GA Enterprise Core â€” Context Accessors
--------------------------------------

LAYER: L1 (Foundation)
Dependencies:
- core.context.request_context
- core.typing
- core.errors.base

Deterministic: YES
Side effects: NONE

Purpose:
- Provide strict, explicit access to request metadata
- Prevent accidental propagation of None values
- Enforce fail-fast semantics at context boundaries

Rules:
- No kernel imports
- MUST raise on missing required metadata
- Accessors contain NO business logic
- Violations MUST raise InvariantViolationError
"""

from afritech.platform.core.context.request_context import RequestContext
from afritech.platform.core.typing import (
    TenantId,
    UserId,
    RequestId,
    CorrelationId,
)
from afritech.platform.core.errors.base import InvariantViolationError


# ============================================================
# Public ABI
# ============================================================

__all__ = [
    "require_tenant_id",
    "require_user_id",
    "require_request_id",
    "require_correlation_id",
]


# ============================================================
# Strict accessors (fail-fast)
# ============================================================

def require_tenant_id(ctx: RequestContext) -> TenantId:
    """
    Require a tenant_id to be present in the request context.
    """
    if ctx.tenant_id is None:
        raise InvariantViolationError(
            "request_context.tenant_id is required",
            metadata={"field": "tenant_id"},
        )
    return ctx.tenant_id


def require_user_id(ctx: RequestContext) -> UserId:
    """
    Require a user_id to be present in the request context.
    """
    if ctx.user_id is None:
        raise InvariantViolationError(
            "request_context.user_id is required",
            metadata={"field": "user_id"},
        )
    return ctx.user_id


def require_request_id(ctx: RequestContext) -> RequestId:
    """
    Require a request_id to be present in the request context.
    """
    if ctx.request_id is None:
        raise InvariantViolationError(
            "request_context.request_id is required",
            metadata={"field": "request_id"},
        )
    return ctx.request_id


def require_correlation_id(ctx: RequestContext) -> CorrelationId:
    """
    Require a correlation_id to be present in the request context.
    """
    if ctx.correlation_id is None:
        raise InvariantViolationError(
            "request_context.correlation_id is required",
            metadata={"field": "correlation_id"},
        )
    return ctx.correlation_id
