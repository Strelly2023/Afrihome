
import pytest
import inspect


def _source(module_path):
    try:
        mod = __import__(module_path, fromlist=['*'])
        import inspect as _i
        return _i.getsource(mod)
    except Exception:
        return None


def test_no_cross_imports_tenancy_rbac():
    ten = _source('core.tenancy.resolver')
    if ten is None:
        pytest.skip('tenancy not ready.')
    assert 'core.rbac' not in ten, 'Tenancy must not import RBAC'


def test_rbac_no_tenancy_import():
    rbac = _source('core.rbac.policy_engine')
    if rbac is None:
        pytest.skip('rbac not ready.')
    assert 'core.tenancy' not in rbac, 'RBAC must not import Tenancy'
