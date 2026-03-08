
"""
GA Enterprise Core — Registry Freeze Guard
------------------------------------------

LAYER: L3+ (LAST)
Dependencies:
- core.kernel.freeze

Rules:
- All mutating operations in registry must call assert_registry_mutable()
- Freeze is global and irreversible (delegated to kernel.freeze)
"""


from core.kernel.freeze import assert_kernel_mutable

def assert_registry_mutable() -> None:
    assert_kernel_mutable()
