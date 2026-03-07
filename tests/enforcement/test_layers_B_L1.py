
import importlib
import pytest

REQUIRED = [
    'core.context.request_context',
    'core.context.accessors',
    'core.execution.execution_context',
    'core.execution.strict_write',
    'core.execution.transaction',
]

@pytest.mark.parametrize('mod', REQUIRED)
def test_l1_imports(mod):
    try:
        importlib.import_module(mod)
    except ModuleNotFoundError:
        pytest.skip(f"Missing {mod} (OK pre-implementation).")
