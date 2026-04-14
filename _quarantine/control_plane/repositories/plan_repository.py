from typing import Protocol, Optional, Tuple
from control_plane.governance.plans.plan import Plan  # adjust path if needed
from typing import Protocol, Optional, runtime_checkable, Iterable


class PlanRepository(Protocol):
    """
    Plans catalog (governance).
    """
    def get(self, plan_id: str) -> Optional[Plan]: ...
    def list(self, *, limit: int = 100, offset: int = 0) -> Tuple[Plan, ...]: ...

    """
    Plan repository (versioned).

    Keys
    ----
    - (plan_key, version) uniquely identifies a Plan.
    """

    def get_by_key_and_version(self, key: str, version: int) -> Optional[Plan]: ...
    def get_latest_by_key(self, key: str) -> Optional[Plan]: ...
    def list_all(self, *, limit: int = 200, offset: int = 0) -> Iterable[Plan]: ...
    def save(self, plan: Plan) -> None: ...