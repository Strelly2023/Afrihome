import ast
from afritech.guards.result import GuardResult


def run(rule: dict, context: dict) -> GuardResult:
    """
    Enforces forbidden imports within the provided scope.

    Scope is already resolved by the executor.
    This guard MUST NOT re-evaluate jurisdiction.
    """
    rule_id = rule["id"]
    rule_type = rule["type"]
    scope = rule.get("scope")
    forbidden = set(rule.get("forbidden", []))

    violations = []
    checked = 0

    for path in context["files"]:
        # Scope is optional; tolerate scope=None
        if scope and not path.startswith(scope):
            continue

        checked += 1

        try:
            with open(path, encoding="utf-8") as f:
                tree = ast.parse(f.read())
        except Exception as exc:
            return GuardResult.errored(
                rule_id=rule_id,
                rule_type=rule_type,
                errors=[f"{path}: parse error ({exc})"],
                checked=checked,
            )

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for name in node.names:
                    base = name.name.split(".")[0]
                    if base in forbidden:
                        violations.append(
                            f"{path}: import '{name.name}'"
                        )

            elif isinstance(node, ast.ImportFrom) and node.module:
                base = node.module.split(".")[0]
                if base in forbidden:
                    violations.append(
                        f"{path}: from '{node.module}'"
                    )

    return GuardResult(
        rule_id=rule_id,
        rule_type=rule_type,
        violations=violations,
        checked=checked,
    )