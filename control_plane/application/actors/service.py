# control_plane/application/actors/service.py
from dataclasses import dataclass
from typing import Mapping, Tuple

from core.errors import ValidationError
from core.kernel.invariants import assert_not_none
from core.rbac.policy_engine import Subject  # types only; no evaluation here
from core.typing import RoleName, UserId

from .mapping import map_headers_to_actor
from .models import Actor, ActorKind


@dataclass(frozen=True, slots=True)
class ActorService:
    """
    Orchestration helpers around Actor (no RBAC decisions, no IO).
    - Map inbound headers -> Actor
    - Provide canonical Subject view for later authorization (3.3)
    - Offer small predicates and guards used by application services
    """

    # --- Construction ---

    @staticmethod
    def from_headers(headers: Mapping[str, str]) -> Actor:
        """
        Deterministically build an Actor from normalized headers.
        """
        assert_not_none(headers, "headers")
        return map_headers_to_actor(headers)

    # --- Translation for Authorization layer (3.3) ---

    @staticmethod
    def to_subject(actor: Actor) -> Subject:
        """
        Create an RBAC Subject view for later deny-wins evaluation (in 3.3).
        No evaluation is performed here.
        """
        assert_not_none(actor, "actor")
        uid: UserId | None = actor.user_id
        return Subject(user_id=uid, roles=tuple(actor.roles))

    # --- Small predicates/guards ---

    @staticmethod
    def is_user(actor: Actor) -> bool:
        return actor.kind is ActorKind.USER

    @staticmethod
    def is_system(actor: Actor) -> bool:
        return actor.kind is ActorKind.SYSTEM

    @staticmethod
    def is_operator(actor: Actor) -> bool:
        return actor.kind is ActorKind.OPERATOR

    @staticmethod
    def require_user(actor: Actor) -> UserId:
        """
        Ensure the actor is a USER and return its UserId deterministically.
        """
        if actor.kind is not ActorKind.USER or actor.user_id is None:
            raise ValidationError("Operation requires USER actor")
        return actor.user_id

    @staticmethod
    def effective_roles(
        actor: Actor, *, default: Tuple[RoleName, ...] = ()
    ) -> Tuple[RoleName, ...]:
        """
        Return the actor's roles or provided defaults (deterministically
        preserving order and uniqueness).
        """
        if actor.roles:
            # Roles already unique/order-preserved from mapping; just return.
            return tuple(actor.roles)
        # De-duplicate defaults deterministically.
        seen = set()
        out: list[RoleName] = []
        for r in default:
            sr = str(r)
            if sr not in seen:
                seen.add(sr)
                out.append(RoleName(sr))
        return tuple(out)
