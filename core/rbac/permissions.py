
"""
GA Enterprise Core — RBAC Permission Matching
---------------------------------------------

LAYER: L3
Dependencies:
- core.rbac.grammar
- core.kernel.invariants
- core.errors

Deterministic: YES
"""


from core.rbac.grammar import (
    validate_permission_name,
    validate_permission_pattern,
)


def permission_matches(pattern: str, permission: str) -> bool:
    p = validate_permission_pattern(pattern)
    s = validate_permission_name(permission)

    ptoks = p.split('.')
    stoks = s.split('.')

    i = j = 0
    while i < len(ptoks) and j < len(stoks):
        tok = ptoks[i]
        if tok == '*':
            i += 1; j += 1; continue
        if tok == '**':
            return True
        if tok == stoks[j]:
            i += 1; j += 1; continue
        return False

    if i == len(ptoks) - 1 and ptoks[-1] == '**':
        return True
    return i == len(ptoks) and j == len(stoks)
