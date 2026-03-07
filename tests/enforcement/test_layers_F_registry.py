import pytest
import importlib

REQUIRED = [
    "core.registry.base",
    "core.registry.scopes",
    "core.registry.services",
    "core.registry.handlers",
    "core.registry.registry",
    "core.registry.freeze_guard",
]


def test_registry_imports_last():
    """
    Registry modules should import only after kernel.freeze exists.
    If kernel.freeze is missing, all registry imports should fail deterministically.
    """
    try:
        importlib.import_module("core.kernel.freeze")
    except ModuleNotFoundError:
        for m in REQUIRED:
            with pytest.raises(ModuleNotFoundError):
                importlib.import_module(m)
        pytest.skip("kernel.freeze missing, registry must be absent (OK).")
        return

    # With kernel.freeze present, registry modules must import cleanly.
    for m in REQUIRED:
        importlib.import_module(m)


def test_freeze_guard_enforced(monkeypatch):
    """
    Registry mutators must refuse to run when the kernel is frozen.
    We simulate the frozen state via monkeypatch to avoid global side effects.
    """
    try:
        from core.kernel.freeze import is_kernel_frozen, KernelFrozenError
        from core.registry.freeze_guard import assert_registry_mutable
        import core.kernel.freeze as kf
    except ModuleNotFoundError:
        pytest.skip("Registry or kernel not implemented yet.")

    # If kernel is already frozen, don't mutate global state further—skip.
    if is_kernel_frozen():
        pytest.skip("Kernel already frozen earlier.")

    # Simulate frozen kernel without calling freeze_kernel()
    monkeypatch.setattr(kf, "_KERNEL_FROZEN", True, raising=True)

    with pytest.raises(KernelFrozenError):
        assert_registry_mutable()