
"""
GA Enterprise Core — Request Context Layer

LAYER: L1

Purpose:
- Immutable request metadata
- Safe access helpers
"""

from .request_context import RequestContext
from .accessors import (
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
