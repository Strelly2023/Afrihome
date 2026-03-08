# control_plane/application/execution/constants.py
"""
AfriHome Control Plane — Application/Execution
PHASE: 3.1 (Orchestration only)
IO: NONE | Threads/async: NONE | Deterministic: YES
"""

# Canonical inbound header names (normalized to lowercase by the factory)
HDR_REQUEST_ID = "x-request-id"
HDR_CORRELATION_ID = "x-correlation-id"
HDR_CAUSATION_ID = "x-causation-id"

HDR_TENANT_ID = "x-tenant-id"
HDR_TENANT_SLUG = "x-tenant-slug"

HDR_ACTOR_KIND = "x-actor-kind"  # USER | API_KEY | SYSTEM | OPERATOR
HDR_USER_ID = "x-user-id"  # required if kind=USER
HDR_ROLES = "x-roles"  # optional, comma-separated
HDR_PRINCIPAL = "x-principal"  # optional, e.g., api key id or service name
