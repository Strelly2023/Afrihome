
import importlib
import pytest
#from .static_import_scanner import build_dependency_edges, project_submodule_name
from tests.enforcement.static_import_scanner import (
    build_dependency_edges,
    project_submodule_name,
)

REQUIRED = [
    'core.errors',
    'core.typing',
    'core.kernel.freeze',
    'core.kernel.invariants',
    'core.identity.uuid',
    'core.time.clock',
    'core.time.hlc',
]

@pytest.mark.parametrize('mod', REQUIRED)
def test_l0_modules_import(mod):
    try:
        importlib.import_module(mod)
    except ModuleNotFoundError:
        pytest.skip(f"Missing {mod} (OK before implementation).")
    except Exception as e:
        pytest.fail(f"{mod} should import cleanly: {e}")


def test_l0_has_no_illegal_cross_deps(core_root, canonical_order):
    modules, edges = build_dependency_edges(core_root)
    for src, dst in edges:
        s = project_submodule_name(src)
        d = project_submodule_name(dst)
        if s in canonical_order and d in canonical_order:
            assert canonical_order[s] < canonical_order[d], (
                f"Layer violation: {s} (#{canonical_order[s]}) must not depend on {d} (#{canonical_order[d]})."
            )
