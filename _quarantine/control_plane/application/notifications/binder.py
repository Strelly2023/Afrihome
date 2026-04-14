from dataclasses import dataclass
from typing import Mapping, Any, Optional
from core.errors import ValidationError
from .models import RenderedMessage

@dataclass(frozen=True, slots=True)
class DefaultTemplateBinder:
    """
    Deterministic, side-effect-free binder using str.format_map with a safe fallback.
    NOTE:
      - Missing variables are rendered as "{name}" (explicit) unless you prefer empty strings.
      - No IO; purely transforms the provided template payload.
    """

    def _fmt(self, s: Optional[str], vars: Mapping[str, Any]) -> Optional[str]:
        if s is None:
            return None

        class _Safe(dict):
            def __missing__(self, key):
                # Keep placeholder visible to aid debugging; deterministic behavior.
                return "{" + key + "}"

        if not isinstance(vars, Mapping):
            raise ValidationError("variables must be a mapping")
        return s.format_map(_Safe(vars))

    def bind(
        self,
        *,
        template_payload: Mapping[str, Any],
        variables: Mapping[str, Any],
    ) -> RenderedMessage:
        subj = self._fmt(template_payload.get("subject"), variables)
        txt  = self._fmt(template_payload.get("body_text"), variables)
        html = self._fmt(template_payload.get("body_html"), variables)
        return RenderedMessage(subject=subj, body_text=txt, body_html=html, variables=dict(variables))