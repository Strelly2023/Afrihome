from dataclasses import dataclass, replace

from control_plane.governance.features.feature_flag import normalize_feature_key
from control_plane.governance.usage.usage_event import normalize_metric_key
from core.errors import InvariantViolationError
from core.typing import TenantId, UnixMillis

from .usage_event import UsageEvent
from .windowing import UsageGranularity, window_end_ms, window_start_ms


@dataclass(frozen=True, slots=True)
class UsageCounter:
    """
    Immutable per-window counter.

    Keys:
      - tenant_id
      - feature_key
      - metric_key
      - granularity
      - window_start_ms

    Values:
      - quantity
      - last_event_ms

    Pure transitions:
      - from_event(event, granularity)
      - apply(event) -> new counter (must be same key/window)
      - merge(other) -> new counter (same key/window)
    """

    tenant_id: TenantId
    feature_key: str
    metric_key: str
    granularity: UsageGranularity
    window_start_ms: UnixMillis

    quantity: int
    last_event_ms: UnixMillis

    def __post_init__(self) -> None:
        fk = normalize_feature_key(self.feature_key)
        mk = normalize_metric_key(self.metric_key)
        object.__setattr__(self, "feature_key", fk)
        object.__setattr__(self, "metric_key", mk)

        if int(self.quantity) < 0:
            raise InvariantViolationError("quantity must be >= 0")

        # Sanity: last_event must be inside [start, end)
        if not (
            int(self.window_start_ms)
            <= int(self.last_event_ms)
            < int(window_end_ms(self.window_start_ms, self.granularity))
        ):
            raise InvariantViolationError("last_event_ms must fall within the counter window")

    # ---------- Constructors ----------

    @staticmethod
    def from_event(event: UsageEvent, granularity: UsageGranularity) -> "UsageCounter":
        start = window_start_ms(event.timestamp_ms, granularity)
        return UsageCounter(
            tenant_id=event.tenant_id,
            feature_key=event.feature_key,
            metric_key=event.metric_key,
            granularity=granularity,
            window_start_ms=start,
            quantity=event.quantity,
            last_event_ms=event.timestamp_ms,
        )

    # ---------- Transitions (pure) ----------

    def _same_key(self, event: UsageEvent) -> bool:
        return (
            self.tenant_id == event.tenant_id
            and self.feature_key == event.feature_key
            and self.metric_key == event.metric_key
        )

    def apply(self, event: UsageEvent) -> "UsageCounter":
        """
        Fold an event into this counter. Event must match keys and window.
        """
        if not self._same_key(event):
            raise InvariantViolationError(
                "UsageCounter.apply: mismatched keys (tenant/feature/metric)"
            )
        start = window_start_ms(event.timestamp_ms, self.granularity)
        if start != self.window_start_ms:
            raise InvariantViolationError(
                "UsageCounter.apply: event is outside this counter's window"
            )
        new_qty = int(self.quantity) + int(event.quantity)
        new_last = (
            event.timestamp_ms
            if int(event.timestamp_ms) > int(self.last_event_ms)
            else self.last_event_ms
        )
        return replace(self, quantity=new_qty, last_event_ms=new_last)

    def merge(self, other: "UsageCounter") -> "UsageCounter":
        """
        Merge two counters with identical keys & window (e.g., reduce from shards).
        """
        if (
            self.tenant_id != other.tenant_id
            or self.feature_key != other.feature_key
            or self.metric_key != other.metric_key
            or self.granularity != other.granularity
            or self.window_start_ms != other.window_start_ms
        ):
            raise InvariantViolationError("UsageCounter.merge: keys/window mismatch")
        new_qty = int(self.quantity) + int(other.quantity)
        new_last = (
            self.last_event_ms
            if int(self.last_event_ms) >= int(other.last_event_ms)
            else other.last_event_ms
        )
        return replace(self, quantity=new_qty, last_event_ms=new_last)
