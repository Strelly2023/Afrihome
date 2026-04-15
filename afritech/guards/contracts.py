from dataclasses import dataclass
from typing import List

@dataclass(frozen=True)
class GuardResult:
    rule_id: str
    violations: List[str]
    fixed: bool
