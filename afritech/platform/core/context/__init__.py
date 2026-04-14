"""
GA Enterprise Core â€” Request Context
-----------------------------------

LAYER: L1 (Foundation)
Deterministic: YES
Side effects: NONE

Purpose:
- Expose immutable request context structures
- Provide explicit, safe accessors for request metadata
- Avoid threadlocals, globals, or hidden state

Rules:
- Context is read-only
- Context carries metadata, not behavior
- Accessors must fail-fast on missing required values
"""

from afritech.platform.core.context.request_context import RequestContext
from afritech.platform.core.context.accessors import (
    require_tenant_id,
    require_user_id,
    require_request_id,
    require_correlation_id,
)

__all__ = [
    "RequestContext",
    "require_tenant_id",
    "require_user_id",
    "require_request_id",
    "require_correlation_id",
]
