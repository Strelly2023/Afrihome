from dataclasses import dataclass
from typing import Tuple

from core.events import EventEnvelope  # immutable, deterministic envelope  # noqa

# (No IO here; outbox persistence happens later in infra.)                     # noqa


@dataclass(frozen=True, slots=True)
class OutboxWrite:
    """
    Immutable instruction to append an event envelope under a specific topic.
    Topic grammar is validated later (core.outbox). No IO is performed here.
    """

    topic: str
    envelope: EventEnvelope


@dataclass(frozen=True, slots=True)
class ReactionPlan:
    """
    Immutable reaction outcome: a set of outbox writes to perform.
    Deterministic and replay-safe.
    """

    writes: Tuple[OutboxWrite, ...] = ()
