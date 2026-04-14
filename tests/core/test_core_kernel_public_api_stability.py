"""
GA Core â€” Kernel Public ABI Stability Test
-----------------------------------------

Purpose:
- Freeze the Kernel (L0) public API forever
- Enforce explicit ABI via __all__
- Block accidental symbol exposure

RULE:
- Kernel ABI is defined ONLY by __all__
- Any change here is a BREAKING CHANGE
"""

import afritech.platform.core.kernel.freeze as freeze
import afritech.platform.core.kernel.invariants as invariants
import afritech.platform.core.kernel.sealed as sealed


def api(module):
    """
    Kernel ABI is defined strictly by __all__.
    """
    assert hasattr(module, "__all__"), (
        f"{module.__name__} must define __all__"
    )
    return sorted(module.__all__)


# ---------------------------------------------------------------------
# freeze.py
# ---------------------------------------------------------------------

def test_kernel_freeze_api_stable():
    expected = sorted([
        "FREEZE_SENTINEL",
        "freeze_kernel",
        "is_kernel_frozen",
        "assert_kernel_not_frozen",
    ])

    assert api(freeze) == expected


# ---------------------------------------------------------------------
# invariants.py
# ---------------------------------------------------------------------

def test_kernel_invariants_api_stable():
    expected = sorted([
        "assert_invariant",
        "assert_not_none",
        "assert_true",
    ])

    assert api(invariants) == expected


# ---------------------------------------------------------------------
# sealed.py
# ---------------------------------------------------------------------

def test_kernel_sealed_api_stable():
    expected = [
        "assert_kernel_sealed",
    ]

    assert api(sealed) == expected
