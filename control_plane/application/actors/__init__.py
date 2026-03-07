#control_plane/application/actors/__init__.py
"""
AfriHome Control Plane — Application/Actors
PHASE: 3.2 (Orchestration only)
IO: NONE | Threads/async: NONE | Deterministic: YES

Exports:
- Header constants (canonical)
- ActorKind, Actor
- map_headers_to_actor (pure mapping, no RBAC)
- ActorService (orchestration helpers; zero business logic)
"""
from .constants import (
    HDR_ACTOR_KIND, HDR_USER_ID, HDR_ROLES, HDR_PRINCIPAL,
)
from .models import ActorKind, Actor
from .mapping import map_headers_to_actor
from .service import ActorService

__all__ = [
    "HDR_ACTOR_KIND", "HDR_USER_ID", "HDR_ROLES", "HDR_PRINCIPAL",
    "ActorKind", "Actor",
    "map_headers_to_actor",
    "ActorService",
]