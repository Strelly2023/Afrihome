"""
GA Core â€” RBAC Property Tests
----------------------------

Purpose:
- Prove semantic correctness of the RBAC engine
- Enforce deny-wins, determinism, and safety invariants
- Guard against behavioral regressions during refactors

These tests validate PROPERTIES, not implementations.
"""

from afritech.platform.core.rbac import (
    Role,
    RBACState,
)
from afritech.platform.core.typing import Permission


# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------

def make_state(*roles, assignments=None) -> RBACState:
    """
    Construct an immutable RBACState deterministically.
    """
    if assignments is None:
        assignments = {}

    state = RBACState(roles={}, assignments={})

    for role in roles:
        state = state.register_role(role)

    for subject_id, role_names in assignments.items():
        for role_name in role_names:
            state = state.assign_role(
                subject_id=subject_id,
                role_name=role_name,
            )

    return state


USER = "user-1"


# ------------------------------------------------------------
# Property 1 â€” Default deny
# ------------------------------------------------------------

def test_default_deny_when_no_roles():
    state = RBACState(roles={}, assignments={})

    assert state.has_for_subject(
        subject_id=USER,
        permission=Permission("invoice.read"),
    ) is False


# ------------------------------------------------------------
# Property 2 â€” Allow grants permission
# ------------------------------------------------------------

def test_allow_grants_permission():
    reader = Role(
        name="reader",
        allow=("invoice.read",),
    )

    state = make_state(
        reader,
        assignments={USER: ("reader",)},
    )

    assert state.has_for_subject(
        subject_id=USER,
        permission=Permission("invoice.read"),
    ) is True

    assert state.has_for_subject(
        subject_id=USER,
        permission=Permission("invoice.write"),
    ) is False


# ------------------------------------------------------------
# Property 3 â€” Deny wins over allow
# ------------------------------------------------------------

def test_deny_wins_over_allow():
    allow_all = Role(
        name="allow_all",
        allow=("invoice.*",),
    )

    deny_read = Role(
        name="deny_read",
        deny=("invoice.read",),
    )

    state = make_state(
        allow_all,
        deny_read,
        assignments={USER: ("allow_all", "deny_read")},
    )

    assert state.has_for_subject(
        subject_id=USER,
        permission=Permission("invoice.read"),
    ) is False

    assert state.has_for_subject(
        subject_id=USER,
        permission=Permission("invoice.update"),
    ) is True


# ------------------------------------------------------------
# Property 4 â€” Role order does NOT matter
# ------------------------------------------------------------

def test_role_order_does_not_affect_decision():
    allow = Role(
        name="allow",
        allow=("invoice.read",),
    )

    deny = Role(
        name="deny",
        deny=("invoice.read",),
    )

    state = make_state(
        allow,
        deny,
        assignments={USER: ("allow", "deny")},
    )

    assert state.has_for_subject(
        subject_id=USER,
        permission=Permission("invoice.read"),
    ) is False


# ------------------------------------------------------------
# Property 5 â€” Unknown roles are ignored (fail-safe)
# ------------------------------------------------------------

def test_unknown_role_is_ignored():
    reader = Role(
        name="reader",
        allow=("invoice.read",),
    )

    state = make_state(
        reader,
        assignments={USER: ("reader", "ghost")},
    )

    assert state.has_for_subject(
        subject_id=USER,
        permission=Permission("invoice.read"),
    ) is True

    assert state.has_for_subject(
        subject_id=USER,
        permission=Permission("invoice.write"),
    ) is False


# ------------------------------------------------------------
# Property 6 â€” Wildcard semantics
# ------------------------------------------------------------

def test_wildcard_behavior():
    role = Role(
        name="wild",
        allow=("invoice.*",),
        deny=("invoice.secret",),
    )

    state = make_state(
        role,
        assignments={USER: ("wild",)},
    )

    assert state.has_for_subject(
        subject_id=USER,
        permission=Permission("invoice.read"),
    ) is True

    assert state.has_for_subject(
        subject_id=USER,
        permission=Permission("invoice.write"),
    ) is True

    assert state.has_for_subject(
        subject_id=USER,
        permission=Permission("invoice.secret"),
    ) is False


# ------------------------------------------------------------
# Property 7 â€” Determinism (idempotence)
# ------------------------------------------------------------

def test_determinism_idempotence():
    role = Role(
        name="det",
        allow=("audit.read",),
    )

    state = make_state(
        role,
        assignments={USER: ("det",)},
    )

    r1 = state.has_for_subject(
        subject_id=USER,
        permission=Permission("audit.read"),
    )
    r2 = state.has_for_subject(
        subject_id=USER,
        permission=Permission("audit.read"),
    )
    r3 = state.has_for_subject(
        subject_id=USER,
        permission=Permission("audit.read"),
    )

    assert r1 is True
    assert r1 == r2 == r3


# ------------------------------------------------------------
# Property 8 â€” Adding deny never grants access
# ------------------------------------------------------------

def test_monotonicity_of_deny():
    allow = Role(
        name="allow",
        allow=("data.*",),
    )

    deny = Role(
        name="deny",
        deny=("data.read",),
    )

    state_allow = make_state(
        allow,
        assignments={USER: ("allow",)},
    )

    state_deny = make_state(
        allow,
        deny,
        assignments={USER: ("allow", "deny")},
    )

    assert state_allow.has_for_subject(
        subject_id=USER,
        permission=Permission("data.read"),
    ) is True

    assert state_deny.has_for_subject(
        subject_id=USER,
        permission=Permission("data.read"),
    ) is False
