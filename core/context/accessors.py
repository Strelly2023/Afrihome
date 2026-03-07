
"""
GA Enterprise Core — Context Accessors
--------------------------------------

LAYER: L1
Dependencies:
- core.context.request_context
- core.errors

Purpose:
- Enforce safe metadata access
- Prevent silent None usage
"""


from core.context.request_context import RequestContext
from core.typing import (
    TenantId,
    UserId,
    RequestId,
    CorrelationId,
)
from core.errors import InvariantViolationError


def require_tenant_id(ctx: RequestContext) -> TenantId:
    if ctx.tenant_id is None:
        raise InvariantViolationError("Tenant ID is required")
    return ctx.tenant_id


def require_user_id(ctx: RequestContext) -> UserId:
    if ctx.user_id is None:
        raise InvariantViolationError("User ID is required")
    return ctx.user_id


def require_request_id(ctx: RequestContext) -> RequestId:
    return ctx.request_id


def require_correlation_id(ctx: RequestContext) -> CorrelationId:
    return ctx.correlation_id
