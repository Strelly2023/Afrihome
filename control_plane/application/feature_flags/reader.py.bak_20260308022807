from dataclasses import dataclass
from typing import Any, Mapping, Optional
from core.kernel.invariants import assert_not_none
from control_plane.application.execution.models import ExecutionFrame
from .resolver import RuleResolver
from .models import FeatureDecision

@dataclass(frozen=True, slots=True)
class FlagReader:
    """
    Thin convenience wrapper over RuleResolver for common read patterns.
    Orchestration-only; no storage or provider access.
    """
    resolver: RuleResolver

    def decision(
        self,
        frame: ExecutionFrame,
        key: str,
        attributes: Mapping[str, Any] | None = None,
    ) -> FeatureDecision:
        assert_not_none(frame, "frame")
        return self.resolver.evaluate(frame, key, attributes)

    def is_enabled(
        self,
        frame: ExecutionFrame,
        key: str,
        attributes: Mapping[str, Any] | None = None,
    ) -> bool:
        return self.decision(frame, key, attributes).enabled

    def get_variant(
        self,
        frame: ExecutionFrame,
        key: str,
        attributes: Mapping[str, Any] | None = None,
        default: Optional[str] = None,
    ) -> Optional[str]:
        dec = self.decision(frame, key, attributes)
        return dec.variant if dec.variant is not None else default