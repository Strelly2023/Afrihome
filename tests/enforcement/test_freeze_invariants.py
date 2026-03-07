import pytest


def test_kernel_freeze_guard_present(monkeypatch):
    """
    Validate the kernel freeze guard without permanently freezing the kernel.
    We simulate _KERNEL_FROZEN via monkeypatch and expect KernelFrozenError.
    """
    try:
        from core.kernel.freeze import assert_kernel_mutable, is_kernel_frozen, KernelFrozenError
        import core.kernel.freeze as kf
    except ModuleNotFoundError:
        pytest.skip("kernel.freeze not implemented yet.")

    # If already frozen (e.g., by a previous suite or environment), skip to avoid side effects.
    if is_kernel_frozen():
        pytest.skip("Kernel already frozen by previous test/environment.")

    # Initially must be mutable.
    assert_kernel_mutable()

    # Simulate freeze state deterministically (no global side effects).
    monkeypatch.setattr(kf, "_KERNEL_FROZEN", True, raising=True)

    # Now guard must raise the explicit platform error type.
    with pytest.raises(KernelFrozenError):
        assert_kernel_mutable()