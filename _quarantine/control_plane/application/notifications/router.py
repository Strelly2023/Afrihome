from dataclasses import dataclass
from typing import Mapping, Tuple
from .models import Channel, ChannelTarget
from .protocols import ChannelRouter

@dataclass(frozen=True, slots=True)
class StaticChannelRouter(ChannelRouter):
    """
    Deterministic router useful for tests and bootstrap defaults.
    Always returns given addresses from attributes (if present).
    """
    def route(
        self,
        *,
        tenant_slug: str,
        attributes: Mapping[str, str],
        variables: Mapping[str, str],
    ) -> Tuple[ChannelTarget, ...]:
        targets: list[ChannelTarget] = []
        if "email_to" in attributes:
            targets.append(ChannelTarget(channel=Channel.EMAIL, address=attributes["email_to"]))
        if "sms_to" in attributes:
            targets.append(ChannelTarget(channel=Channel.SMS, address=attributes["sms_to"]))
        if "webhook_url" in attributes:
            targets.append(ChannelTarget(channel=Channel.WEBHOOK, address=attributes["webhook_url"]))
        return tuple(targets)