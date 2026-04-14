import pytest

from afritech.platform.core.decision.combinator import combine
from afritech.platform.core.errors import InvariantViolationError


def test_empty_outcomes_with_allows_is_invalid():
    """
    ✅ Fail‑Closed Semantics — Empty Outcomes With Allows (GA‑Sealed)

    Guarantees:
    - Empty EngineOutcome sets are always invalid
    - ALLOW cannot be implied or assumed
    - The system refuses to fabricate decisions
    """

    # Caller provides no EngineOutcome objects at all.
    # Even if the caller *intends* an allow, this is invalid.
    outcomes = ()

    # ✅ Fail‑closed: reject empty evaluation
    with pytest.raises(InvariantViolationError):
        combine(outcomes)