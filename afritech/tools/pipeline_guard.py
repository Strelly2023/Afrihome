from typing import List, Sequence

from afritech.guards.result import GuardResult


def run(rule: dict, context: dict) -> GuardResult:
    """
    Enforcement guard for decision pipeline ordering (DEC-001).

    Law:
        Decision engines MUST execute in the exact order defined
        by the governing rule.

    This guard enforces *ordering only*.
    Execution completeness (no short-circuit) is enforced separately.
    """

    rule_id = rule["id"]
    rule_type = rule["type"]

    expected: List[str] = rule.get("order", [])
    actual: Sequence[str] | None = context.get("pipeline")

    # ------------------------------------------------------------
    # Defensive: missing pipeline context is an ENFORCEMENT ERROR
    # ------------------------------------------------------------
    if actual is None:
        return GuardResult.errored(
            rule_id=rule_id,
            rule_type=rule_type,
            errors=[
                "Decision pipeline not provided in execution context"
            ],
            checked=0,
        )

    # Defensive: pipeline must be a sequence of identifiers
    if not isinstance(actual, (list, tuple)):
        return GuardResult.errored(
            rule_id=rule_id,
            rule_type=rule_type,
            errors=[
                f"Invalid pipeline type: expected sequence, got {type(actual).__name__}"
            ],
            checked=0,
        )

    # ------------------------------------------------------------
    # Rule enforcement: STRICT order equality
    # ------------------------------------------------------------
    if list(actual) != expected:
        return GuardResult.failure(
            rule_id=rule_id,
            rule_type=rule_type,
            violations=[
                f"Expected pipeline order {expected}, got {list(actual)}"
            ],
            checked=len(actual),
        )

    # ------------------------------------------------------------
    # Success
    # ------------------------------------------------------------
    return GuardResult.success(
        rule_id=rule_id,
        rule_type=rule_type,
        checked=len(actual),
    )