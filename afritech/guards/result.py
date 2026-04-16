from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, List, Optional


@dataclass(frozen=True)
class GuardResult:
    """
    Canonical result of enforcing a single rule.

    This object is:
    - Immutable (frozen)
    - Serializable
    - Aggregation-safe
    - CI / reporting ready
    - Free of side effects

    Guards MUST return this type.
    """

    # -----------------------------------------------------------------
    # Identity
    # -----------------------------------------------------------------
    rule_id: str
    rule_type: Optional[str] = None

    # -----------------------------------------------------------------
    # Rule-level outcomes
    # -----------------------------------------------------------------
    violations: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    # -----------------------------------------------------------------
    # Tool / execution failures (not rule violations)
    # -----------------------------------------------------------------
    errors: List[str] = field(default_factory=list)

    # -----------------------------------------------------------------
    # Metadata
    # -----------------------------------------------------------------
    fixed: bool = False
    checked: int = 0  # number of files / entities evaluated

    # -----------------------------------------------------------------
    # Derived state
    # -----------------------------------------------------------------
    @property
    def passed(self) -> bool:
        """
        True only if the rule ran successfully and produced no violations.
        """
        return not self.violations and not self.errors

    @property
    def failed(self) -> bool:
        return not self.passed

    @property
    def has_warnings(self) -> bool:
        return bool(self.warnings)

    @property
    def total_issues(self) -> int:
        """
        Total number of failures (violations + execution errors).
        """
        return len(self.violations) + len(self.errors)

    @property
    def is_empty_run(self) -> bool:
        """
        True if the rule evaluated nothing.
        Useful for detecting broken scope or misconfigured tools.
        """
        return self.checked == 0

    # -----------------------------------------------------------------
    # Boolean semantics
    # -----------------------------------------------------------------
    def __bool__(self) -> bool:
        """
        Allow `if result:` to mean "rule passed".
        """
        return self.passed

    # -----------------------------------------------------------------
    # Factory helpers
    # -----------------------------------------------------------------
    @classmethod
    def success(
        cls,
        rule_id: str,
        rule_type: Optional[str] = None,
        *,
        checked: int = 0,
    ) -> GuardResult:
        return cls(
            rule_id=rule_id,
            rule_type=rule_type,
            checked=checked,
        )

    @classmethod
    def failure(
        cls,
        rule_id: str,
        violations: Iterable[str],
        rule_type: Optional[str] = None,
        *,
        checked: int = 0,
    ) -> GuardResult:
        return cls(
            rule_id=rule_id,
            rule_type=rule_type,
            violations=list(violations),
            checked=checked,
        )

    @classmethod
    def errored(
        cls,
        rule_id: str,
        errors: Iterable[str],
        rule_type: Optional[str] = None,
        *,
        checked: int = 0,
    ) -> GuardResult:
        return cls(
            rule_id=rule_id,
            rule_type=rule_type,
            errors=list(errors),
            checked=checked,
        )

    # -----------------------------------------------------------------
    # Aggregation
    # -----------------------------------------------------------------
    def merge(self, other: GuardResult) -> GuardResult:
        """
        Merge two results from the SAME rule.
        """
        if self.rule_id != other.rule_id:
            raise ValueError("Cannot merge GuardResults with different rule IDs")

        if (
            self.rule_type
            and other.rule_type
            and self.rule_type != other.rule_type
        ):
            raise ValueError("Mismatched rule_type in merge")

        return GuardResult(
            rule_id=self.rule_id,
            rule_type=self.rule_type or other.rule_type,
            violations=self.violations + other.violations,
            warnings=self.warnings + other.warnings,
            errors=self.errors + other.errors,
            fixed=self.fixed or other.fixed,
            checked=self.checked + other.checked,
        )

    # -----------------------------------------------------------------
    # Ergonomics
    # -----------------------------------------------------------------
    def with_warnings(self, warnings: Iterable[str]) -> GuardResult:
        """
        Return a copy of this result with additional warnings attached.
        """
        return GuardResult(
            rule_id=self.rule_id,
            rule_type=self.rule_type,
            violations=self.violations,
            warnings=self.warnings + list(warnings),
            errors=self.errors,
            fixed=self.fixed,
            checked=self.checked,
        )

    # -----------------------------------------------------------------
    # Serialization (stable external boundary)
    # -----------------------------------------------------------------
    def to_dict(self) -> dict:
        """
        Stable serialization boundary for JSON reporting / CI artifacts.
        """
        return {
            "rule_id": self.rule_id,
            "rule_type": self.rule_type,
            "violations": list(self.violations),
            "warnings": list(self.warnings),
            "errors": list(self.errors),
            "fixed": self.fixed,
            "checked": self.checked,
            "passed": self.passed,
        }

    @classmethod
    def from_dict(cls, data: dict) -> GuardResult:
        """
        Rehydrate a GuardResult from serialized form.
        """
        return cls(
            rule_id=data["rule_id"],
            rule_type=data.get("rule_type"),
            violations=data.get("violations", []),
            warnings=data.get("warnings", []),
            errors=data.get("errors", []),
            fixed=data.get("fixed", False),
            checked=data.get("checked", 0),
        )

    # -----------------------------------------------------------------
    # Consistency checks (debug / test use only)
    # -----------------------------------------------------------------
    def assert_consistent(self) -> None:
        """
        Internal sanity checks to catch invalid states early.
        """
        if self.passed and (self.violations or self.errors):
            raise AssertionError("Invalid state: passed but contains issues")

        if self.checked < 0:
            raise AssertionError("Invalid checked count")

    # -----------------------------------------------------------------
    # CI / CLI rendering
    # -----------------------------------------------------------------
    def summary(self) -> str:
        """
        Compact one-line summary for CI output or dashboards.
        """
        status = "PASS" if self.passed else "FAIL"
        return (
            f"{self.rule_id} [{status}] "
            f"violations={len(self.violations)} "
            f"errors={len(self.errors)} "
            f"checked={self.checked}"
        )

    def format(self) -> List[str]:
        """
        Render grouped, human-readable output.

        Guards must NEVER print directly.
        """
        lines: List[str] = []

        if self.violations:
            lines.append(f"[{self.rule_id}] ❌ Violations:")
            lines.extend(f"  - {v}" for v in self.violations)

        if self.warnings:
            lines.append(f"[{self.rule_id}] ⚠️ Warnings:")
            lines.extend(f"  - {w}" for w in self.warnings)

        if self.errors:
            lines.append(f"[{self.rule_id}] 💥 Errors:")
            lines.extend(f"  - {e}" for e in self.errors)

        if not lines:
            lines.append(f"[{self.rule_id}] ✅ Passed ({self.checked} checked)")

        return lines
