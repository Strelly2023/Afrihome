import pytest

from afritech.platform.core.decision.combinator import combine
from afritech.platform.core.errors import InvariantViolationError


def test_deny_with_no_outcomes():
    """
    ✅ Fail‑Closed Semantics — No Outcomes (GA‑Sealed)

    Guarantees:
    - The decision system refuses to operate with zero EngineOutcome objects
    - No implicit ALLOW or fabricated DENY is permitted
    - The system fails closed via a hard invariant violation
    """

    outcomes = ()

    # ✅ Fail‑closed at the entry boundary
    with pytest.raises(InvariantViolationError):
        combine(outcomes)
