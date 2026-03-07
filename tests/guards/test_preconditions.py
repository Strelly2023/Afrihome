
import pytest
from core.guards import require, require_present, require_non_empty_str, require_equal, require_allowed
from core.errors import InvariantViolationError, ValidationError, AuthorizationError


def test_preconditions():
    require(True, 'ok')
    with pytest.raises(InvariantViolationError):
        require(False, 'bad')
    require_present(0, 'x')
    with pytest.raises(ValidationError):
        require_non_empty_str('   ', 'name')
    with pytest.raises(InvariantViolationError):
        require_equal(1, 2)
    with pytest.raises(AuthorizationError):
        require_allowed(False)
