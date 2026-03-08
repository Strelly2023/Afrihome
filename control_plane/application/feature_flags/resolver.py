from dataclasses import dataclass
from typing import Any, Mapping

from control_plane.application.execution.models import ExecutionFrame
from core.errors import ValidationError
from core.kernel.invariants import assert_not_none
from core.typing import UnixMillis

from .models import DecisionSource, FeatureDecision
from .protocols import FeatureRuleEvaluator


@dataclass(frozen=True, slots=True)
class RuleResolver:
    """
    Deterministically resolves a feature decision using a pure FeatureRuleEvaluator.
    No IO, no storage, no business logic here—just orchestration.
    """

    evaluator: FeatureRuleEvaluator

    def evaluate(
        self,
        frame: ExecutionFrame,
        key: str,
        attributes: Mapping[str, Any] | None = None,
    ) -> FeatureDecision:
        assert_not_none(frame, "frame")
        assert_not_none(key, "key")

        if not key.strip():
            raise ValidationError("feature key must be a non-empty string")

        attrs = attributes or {}
        now: UnixMillis = frame.ctx.now()

        enabled, variant, reason = self.evaluator.evaluate(
            tenant_id=frame.tenant_id,
            snapshot=frame.feature_snapshot,  # opaque snapshot from 3.1
            actor=frame.actor,
            key=key.strip(),
            attributes=attrs,
            now_ms=now,
        )

        return FeatureDecision(
            key=key.strip(),
            enabled=bool(enabled),
            variant=variant,
            reason=reason,
            source=DecisionSource.RULE,
            attributes=attrs,
        )
