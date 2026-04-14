from dataclasses import dataclass
from typing import Mapping, Any

@dataclass(frozen=True, slots=True)
class AuditPolicy:
    """
    Governance redaction rules applied before persistence.
    """
    redact_fields: tuple[str, ...] = ()

    def apply(self, data: Mapping[str, Any]) -> Mapping[str, Any]:
        # Return a shallow-redacted copy deterministically.
        redacted = dict(data)
        for f in self.redact_fields:
            if f in redacted:
                redacted[f] = "<redacted>"
        return redacted