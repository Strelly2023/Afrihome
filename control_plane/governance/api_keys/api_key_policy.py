from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class ApiKeyPolicy:
    """
    Governance constraints for machine identities.
    (Extend as needed — e.g., ip rules, environment gates, rotation windows.)
    """
    allow_service_accounts: bool = True
    require_rotation_days: int = 0   # 0 = no requirement