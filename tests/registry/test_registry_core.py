
import pytest
from core.registry import CoreRegistry, RegistryScope, DEFAULT_SCOPE_CHAIN
from core.kernel import freeze_kernel, is_kernel_frozen
from core.errors import KernelFrozenError


def test_service_resolution_by_scope_chain():
    reg = CoreRegistry.create()
    reg.services.register_instance('cfg', {'v': 1}, scope=RegistryScope.PROCESS)
    reg.services.register_instance('cfg', {'v': 2}, scope=RegistryScope.APPLICATION)
    reg.services.register_instance('cfg', {'v': 3}, scope=RegistryScope.REQUEST)
    val = reg.services.resolve('cfg', scope_chain=DEFAULT_SCOPE_CHAIN)
    assert val == {'v': 3}


def test_handler_ordering_and_scopes():
    reg = CoreRegistry.create()
    calls = []
    def h1(e): calls.append(('P','h1'))
    def h2(e): calls.append(('A','h2'))
    def h3(e): calls.append(('R','h3'))
    reg.handlers.register('user.created', h1, scope=RegistryScope.PROCESS)
    reg.handlers.register('user.created', h2, scope=RegistryScope.APPLICATION)
    reg.handlers.register('user.created', h3, scope=RegistryScope.REQUEST)
    handlers = reg.handlers.list_for('user.created')
    for h in handlers: h(object())
    assert [c[0] for c in calls] == ['R','A','P']


def test_freeze_blocks_mutation():
    reg = CoreRegistry.create()
    # If already frozen, skip this test
    if is_kernel_frozen():
        pytest.skip('kernel already frozen')
    reg.services.register_instance('x', 1)
    freeze_kernel()
    with pytest.raises(KernelFrozenError):
        reg.services.register_instance('x', 2)
    with pytest.raises(KernelFrozenError):
        reg.handlers.register('k', lambda e: None)
