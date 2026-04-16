from pathlib import Path
import yaml

from afritech.guards.registry import TOOL_MAP, is_test_only
from afritech.guards.scope import collect_files
from afritech.guards.result import GuardResult


def run_all() -> None:
    """
    Execute all constitutional rules.

    This function is the *single authoritative executor* for governance.
    It performs:
      - rule loading
      - schema validation
      - law → tool dispatch
      - scope normalization
      - result aggregation
      - final pass/fail decision

    Contract:
      - No file discovery happens here (scope.py owns that)
      - No enforcement logic lives here (tools own that)
      - No rule silently skips enforcement
    """
    print("🏛 AfriTech Constitutional Guard Runner")

    all_files = collect_files()
    failures: list[GuardResult] = []

    # -----------------------------------------------------------------
    # Load and execute rule files
    # -----------------------------------------------------------------
    for rule_file in sorted(Path("rules").glob("*.yaml")):
        try:
            raw = yaml.safe_load(rule_file.read_text())
        except Exception as exc:
            raise RuntimeError(
                f"Invalid YAML in {rule_file.name}: {exc}"
            )

        # --------------------------------------------------------------
        # Skip empty or comment-only rule files
        # --------------------------------------------------------------
        if raw is None:
            continue

        # --------------------------------------------------------------
        # Enforce minimal rule-file schema
        # --------------------------------------------------------------
        if not isinstance(raw, dict):
            raise RuntimeError(
                f"Invalid rule file {rule_file.name}: root must be a mapping"
            )

        raw_scope = raw.get("scope")
        rules = raw.get("rules")

        if rules is None:
            raise RuntimeError(
                f"Invalid rule file {rule_file.name}: missing 'rules' key"
            )

        if not isinstance(rules, list):
            raise RuntimeError(
                f"Invalid rule file {rule_file.name}: 'rules' must be a list"
            )

        # --------------------------------------------------------------
        # Normalize scope for execution
        #
        # Law-level scope may be structured YAML, but tools only receive
        # executable scope (string or None).
        # --------------------------------------------------------------
        if isinstance(raw_scope, str):
            normalized_scope = raw_scope
        else:
            normalized_scope = None

        # --------------------------------------------------------------
        # Execute individual rules
        # --------------------------------------------------------------
        for rule in rules:
            rule_id = rule.get("id")
            rule_type = rule.get("type")

            if not rule_id or not rule_type:
                raise RuntimeError(
                    f"Malformed rule in {rule_file.name}: {rule}"
                )

            # Inject normalized scope for tools
            rule["scope"] = normalized_scope

            # Skip static execution for test-only rules
            if is_test_only(rule_type):
                continue

            tool = TOOL_MAP.get(rule_type)
            if not tool:
                raise RuntimeError(
                    f"No tool registered for rule type "
                    f"'{rule_type}' ({rule_id})"
                )

            result = tool.run(rule, {"files": all_files})

            if result.failed:
                failures.append(result)

    # -----------------------------------------------------------------
    # Final decision
    # -----------------------------------------------------------------
    if failures:
        print("\n❌ GOVERNANCE VIOLATIONS DETECTED\n")
        for result in failures:
            for line in result.format():
                print(line)
        raise SystemExit(1)

    print("✅ All constitutional rules satisfied")