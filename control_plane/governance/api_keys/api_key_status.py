from enum import Enum, auto


class ApiKeyStatus(Enum):
    ACTIVE = auto()
    SUSPENDED = auto()
    REVOKED = auto()
