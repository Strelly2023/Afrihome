from __future__ import annotations

"""
AfriTech Core Events â€” Finance Domain Events (GA-Sealed)
"""

from dataclasses import dataclass
from afritech.platform.core.events.base import DomainEvent
from afritech.platform.core.events.types import EventType


@dataclass(frozen=True, slots=True)
class PaymentProcessed(DomainEvent):
    payment_id: str
    amount: int
    currency: str
    status: str

    def __init__(
        self,
        *,
        payment_id: str,
        amount: int,
        currency: str,
        status: str,
    ):
        super().__init__(
            event_type=EventType.PAYMENT_PROCESSED,
            payload={
                "payment_id": payment_id,
                "amount": amount,
                "currency": currency,
                "status": status,
            },
        )
