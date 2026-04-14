import pytest

from afritech.platform.core.decision import Decision, DecisionVerdict
from afritech.platform.core.decision.engine_outcome import EngineOutcome
from afritech.platform.core.typing.enums import EngineId, DecisionVerdictType
from afritech.platform.core.errors import InvariantViolationError


class DecisionGateway:
    """
    Minimal execution gateway used ONLY for testing.

    RULE:
    - Execution MUST receive a canonical Decision
    - Raw inputs or engine outcomes are NOT sufficient
    """

    def execute(self, *, decision: Decision) -> None:
        if decision is None:
            raise InvariantViolationError(
                "Execution requires a Decision"
            )

        if not isinstance(decision, Decision):
            raise InvariantViolationError(
                "Invalid decision type"
            )

        if decision.verdict not in (
            DecisionVerdict.ALLOW,
            DecisionVerdict.DENY,
        ):
            raise InvariantViolationError(
                "Decision must be ALLOW or DENY"
            )

        # ✅ Execution permitted (no-op for test)


def test_execution_requires_decision():
    """
    ✅ Decision Gateway Enforcement

    This test proves:
    - Execution CANNOT occur without a Decision
    - Execution WILL accept a canonical Decision
    """

    gateway = DecisionGateway()

    # ❌ Case 1: No decision provided
    with pytest.raises(InvariantViolationError):
        gateway.execute(decision=None)

    # ❌ Case 2: Wrong type provided
    with pytest.raises(InvariantViolationError):
        gateway.execute(decision={"verdict": "allow"})

    # ✅ Case 3: Proper Decision provided
    decision = Decision(
        verdict=DecisionVerdict.ALLOW,
        reasons=(),
        traces=(),
    )

    gateway.execute(decision=decision)
