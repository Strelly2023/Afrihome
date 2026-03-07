#control_plane/repositories.webhook_verification_repository.py
from typing import Protocol, Optional, runtime_checkable, Iterable

from control_plane.governance.integrations.webhook_verification import WebhookVerification



@runtime_checkable
class WebhookVerificationRepository(Protocol):
    """
    Webhook verification policy repository.
    """

    def get_by_provider(self, provider_key: str) -> Optional[WebhookVerification]: ...
    def list_all(self, *, limit: int = 200, offset: int = 0) -> Iterable[WebhookVerification]: ...
    def save(self, policy: WebhookVerification) -> None: ...