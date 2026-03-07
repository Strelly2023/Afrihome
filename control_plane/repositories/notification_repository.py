from typing import Protocol, Mapping, Any, Optional
from control_plane.application.notifications.models import TemplateRef  # app model is pure
from typing import Protocol, Optional, runtime_checkable, Iterable

from control_plane.governance.notifications.template import NotificationTemplate

class NotificationRepository(Protocol):
    """
    Template repository port for notifications (no IO here).
    Application binder uses this port; infra implements it.
    """
    def get_template(self, ref: TemplateRef) -> Optional[Mapping[str, Any]]: ...
    """
    Templates repository (versioned per key if you choose to support that).
    """

    def get_by_key_and_version(self, key: str, version: int) -> Optional[NotificationTemplate]: ...
    def get_latest_by_key(self, key: str) -> Optional[NotificationTemplate]: ...
    def list_all(self, *, limit: int = 200, offset: int = 0) -> Iterable[NotificationTemplate]: ...
    def save(self, tmpl: NotificationTemplate) -> None: ...