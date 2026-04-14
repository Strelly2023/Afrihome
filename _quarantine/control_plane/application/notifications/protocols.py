from typing import Protocol, runtime_checkable, Mapping, Any, Optional, Tuple
from .models import TemplateRef, RenderedMessage, ChannelTarget

@runtime_checkable
class TemplateRepository(Protocol):
    """
    Pure repository interface to retrieve template content/metadata.
    Implementations live in infra (Phase 5); app uses only this contract.
    """
    def get(self, ref: TemplateRef) -> Mapping[str, Any]:
        """
        Returns a mapping with keys like:
          - "subject": str|None
          - "body_text": str|None
          - "body_html": str|None
          - "placeholders": Tuple[str, ...]
        Exact schema is owned by the infra-side repo; app binder treats it opaquely.
        """
        ...

@runtime_checkable
class TemplateBinder(Protocol):
    """
    Pure binder interface. No IO; renders strings deterministically.
    """
    def bind(
        self,
        *,
        template_payload: Mapping[str, Any],
        variables: Mapping[str, Any],
    ) -> RenderedMessage: ...

@runtime_checkable
class ChannelRouter(Protocol):
    """
    Pure per-tenant routing. Given inputs, return where to send.
    No IO; no provider logic.
    """
    def route(
        self,
        *,
        tenant_slug: str,
        attributes: Mapping[str, Any],
        variables: Mapping[str, Any],
    ) -> Tuple[ChannelTarget, ...]: ...