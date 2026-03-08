"""
GA Enterprise Core — Request Context Layer

LAYER: L1

Purpose:
- Immutable request metadata
- Safe access helpers
"""

from .accessors import (
    require_correlation_id,
    require_request_id,
    require_tenant_id,
    require_user_id,
)
from .request_context import RequestContext

__all__ = [
    "RequestContext",
    "require_tenant_id",
    "require_user_id",
    "require_request_id",
    "require_correlation_id",
]
