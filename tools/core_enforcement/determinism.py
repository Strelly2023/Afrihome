from __future__ import annotations
# tools/core_enforcement/determinism.py
"""
Determinism enforcement helpers for AfriTech Core (GA).

This module provides utilities to verify that core logic is:
- deterministic
- replay-safe
- side-effect free

IMPORTANT:
- Test support ONLY
- MUST NOT import anything from afritech.platform.core
- MUST NOT be used at runtime
"""

from dataclasses import is_dataclass
from typing import Any, Callable, Iterable, Tuple

# ---------------------------------------------------------------------
# Core determinism helpers
# ---------------------------------------------------------------------

def replay(
    fn: Callable[..., Any],
    *args: Any,
    **kwargs: Any,
) -> Tuple[Any, Any]:
    """
    Execute the same function twice with identical inputs.

    Returns:
        (first_result, second_result)

    This is the fundamental primitive for determinism checks.
    """
    return fn(*args, **kwargs), fn(*args, **kwargs)


def assert_deterministic(
    fn: Callable[..., Any],
    *args: Any,
    **kwargs: Any,
) -> Any:
    """
    Assert that a function is deterministic under identical inputs.

    Returns:
        the result (if deterministic)

    Raises:
        AssertionError if results differ.
    """
    first, second = replay(fn, *args, **kwargs)

    assert first == second, (
        "Non-deterministic behavior detected:\n"
        f"first  = {first!r}\n"
        f"second = {second!r}"
    )

    return first


# ---------------------------------------------------------------------
# Structural immutability helpers
# ---------------------------------------------------------------------

def assert_immutable(value: Any) -> None:
    """
    Assert that a value is structurally immutable.

    Best-effort guard (not a full formal proof).

    Rules:
    - dataclasses must be frozen
    - list / dict / set are forbidden
    """
    if is_dataclass(value):
        frozen = getattr(value.__dataclass_params__, "frozen", False)
        assert frozen, f"Dataclass {type(value).__name__} is not frozen"
        return

    mutable_types = (list, dict, set)
    assert not isinstance(value, mutable_types), (
        f"Mutable return type detected: {type(value).__name__}"
    )


# ---------------------------------------------------------------------
# Collection determinism helpers
# ---------------------------------------------------------------------

def assert_order_independent(
    fn: Callable[..., Iterable[Any]],
    *args: Any,
    **kwargs: Any,
) -> None:
    """
    Assert that an iterable-producing function is order-stable
    under replay.

    The function MUST return an iterable.
    """
    first, second = replay(fn, *args, **kwargs)

    assert list(first) == list(second), (
        "Order instability detected in iterable result"
    )


# ---------------------------------------------------------------------
# Decision determinism helpers
# ---------------------------------------------------------------------

def assert_decision_deterministic(
    fn: Callable[..., Any],
    *args: Any,
    **kwargs: Any,
) -> Any:
    """
    Specialized helper for decision / policy engines.

    Enforces:
    - deterministic output
    - immutable result
    """
    result = assert_deterministic(fn, *args, **kwargs)
    assert_immutable(result)
    return result


# ---------------------------------------------------------------------
# Forbidden side-effect sentinels (state comparison)
# ---------------------------------------------------------------------

def assert_no_side_effects(
    before: Any,
    after: Any,
    description: str = "state",
) -> None:
    """
    Assert that no external state was modified.

    Typical use:
        before = copy.deepcopy(state)
        fn(...)
        after = state
        assert_no_side_effects(before, after)
    """
    assert before == after, (
        f"Side effect detected on {description}:\n"
        f"before = {before!r}\n"
        f"after  = {after!r}"
    )
