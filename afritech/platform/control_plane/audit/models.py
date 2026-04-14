from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Tuple

from afritech.platform.core.decision.reason import DecisionReason


@dataclass(frozen=True)
class ExecutionAuditRecord:
    """
    Immutable record of an executed action.

    This is the binding between:
    - decision (truth)
    - execution (action)
    """

    decision_id: str
    actor: str
    action: str
    resource: str
    reasons: Tuple[DecisionReason, ...]
    timestamp: datetime