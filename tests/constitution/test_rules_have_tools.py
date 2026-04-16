from pathlib import Path
import yaml
import pytest

from afritech.guards.registry import TOOL_MAP, TEST_ONLY_RULES

"""
This test enforces a core governance invariant (META-002):

    Every rule declared in rules/*.yaml MUST have a declared
    enforcement mechanism, either:
      - a registered tool, OR
      - an explicit test-only designation.

This test prevents "paper rules" that claim authority
without real or declared enforcement.
"""

RULES_DIR = Path("rules")


def test_all_rules_have_declared_enforcement():
    """
    Ensure that every rule type is either:
    - mapped to a tool in TOOL_MAP, OR
    - explicitly declared as test-only in TEST_ONLY_RULES
    """
    assert RULES_DIR.exists(), "Rules directory does not exist"

    rule_files = sorted(RULES_DIR.glob("*.yaml"))
    assert rule_files, "No rule files found in rules/"

    for rule_file in rule_files:
        try:
            data = yaml.safe_load(rule_file.read_text())
        except Exception as exc:
            pytest.fail(f"{rule_file.name} is not valid YAML: {exc}")

        # Empty or comment-only rule files are allowed
        if data is None:
            continue

        assert isinstance(
            data, dict
        ), f"{rule_file.name} root must be a mapping"

        rules = data.get("rules")
        assert rules is not None, f"{rule_file.name} missing 'rules' key"
        assert isinstance(
            rules, list
        ), f"{rule_file.name} 'rules' must be a list"

        for rule in rules:
            rule_id = rule.get("id")
            rule_type = rule.get("type")

            assert rule_id, f"{rule_file.name} contains rule without id"
            assert rule_type, f"{rule_file.name} rule {rule_id} missing type"

            assert (
                rule_type in TOOL_MAP
                or rule_type in TEST_ONLY_RULES
            ), (
                f"Rule {rule_id} ({rule_type}) "
                f"has no enforcement: "
                f"not in TOOL_MAP and not test-only"
            )
