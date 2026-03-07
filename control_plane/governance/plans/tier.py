from dataclasses import dataclass
from enum import Enum, auto
import re

from core.errors import InvariantViolationError


_TIER_CODE_RE = re.compile(r"^[a-z][a-z0-9]*(?:[._-][a-z0-9]+)*$")


def normalize_tier_code(code: str) -> str:
    if not isinstance(code, str):
        raise InvariantViolationError("Tier code must be a string")
    c = code.strip().lower()
    if not _TIER_CODE_RE.match(c):
        raise InvariantViolationError(f"Invalid tier code: {code!r}")
    return c


class BillingCycle(Enum):
    MONTHLY = auto()
    ANNUAL = auto()


@dataclass(frozen=True, slots=True)
class TierMeta:
    """
    Pure metadata for a Plan's tier.

    - code          : canonical tier code (e.g., "free", "pro", "enterprise-eu")
    - name          : display name (human-friendly, validated)
    - description   : optional
    - billing_cycle : cadence (governance signal; app/infra implements billing)
    - currency      : ISO 4217 code (string; governance metadata)
    - price_minor   : non-negative integer cost in minor units (e.g., cents)
    - trial_days    : non-negative days
    - display_order : integer used for UI ordering (lower means earlier)

    NOTE: No money math here; it's purely metadata for downstream systems.
    """
    code: str
    name: str
    billing_cycle: BillingCycle
    currency: str
    price_minor: int

    description: str = ""
    trial_days: int = 0
    display_order: int = 0

    def __post_init__(self) -> None:
        c = normalize_tier_code(self.code)
        object.__setattr__(self, "code", c)

        n = (self.name or "").strip()
        if not n:
            raise InvariantViolationError("Tier name cannot be empty")
        if len(n) > 120:
            raise InvariantViolationError("Tier name too long")
        object.__setattr__(self, "name", n)

        cur = (self.currency or "").upper().strip()
        if not cur or len(cur) not in (3, 4):  # e.g., "USD", or some crypto/alt notation later
            raise InvariantViolationError("currency must be 3-4 uppercase characters")
        object.__setattr__(self, "currency", cur)

        price = int(self.price_minor)
        if price < 0:
            raise InvariantViolationError("price_minor must be >= 0")
        object.__setattr__(self, "price_minor", price)

        td = int(self.trial_days)
        if td < 0:
            raise InvariantViolationError("trial_days must be >= 0")
        object.__setattr__(self, "trial_days", td)

        # display_order can be negative for custom ordering but keep it int.
        _ = int(self.display_order)