"""
AfriTech Core Enforcement Rules (GAâ€‘Sealed)
==========================================

This file is the SINGLE SOURCE OF TRUTH for what is allowed inside
afritech.platform.core.

Any change to this file is a BREAKING ARCHITECTURAL DECISION
and REQUIRES a formal ADR.

These rules are enforced mechanically by CI and tests.
"""


# ---------------------------------------------------------------------
# Core root path
# ---------------------------------------------------------------------
# NOTE:
# This is intentionally a STRING.
# Tooling is responsible for resolving it to Path objects.
# ---------------------------------------------------------------------

CORE_ROOT = "afritech/platform/core"


# ---------------------------------------------------------------------
# Canonical Core Import Rules
# ---------------------------------------------------------------------
# Meaning:
#   key   = top-level core module (directory under CORE_ROOT)
#   value = list of other core modules it MAY import
#
# Any import not declared here is a GA violation.
# ---------------------------------------------------------------------

CORE_IMPORT_RULES = {

    # ================================================================
    # L0 â€” Kernel (absolute invariants, fatal authority)
    # ================================================================
    # Kernel MUST NOT import anything from core (including errors).
    # ================================================================
    "kernel": [],


    # ================================================================
    # L1 â€” Deterministic Foundations
    # ================================================================
    # These modules define language, grammar, and value primitives.
    # They may depend ONLY on lower-level foundations.
    # ================================================================

    "errors": [],                         # error taxonomy ONLY
    "typing": ["errors"],                 # value shapes + validation
    "time": ["typing", "errors"],         # time VALUES only (never clocks)
    "identity": ["typing", "errors"],     # identity MODELS only
    "context": ["typing", "identity", "errors"],
    "tenancy": ["typing", "errors"],      # grammar ONLY (no resolution)


    # ================================================================
    # L2 â€” Governance / Protocol / Metadata
    # ================================================================
    # These are NOT decision engines.
    # They define invariants, contracts, and immutable structures.
    # ================================================================

    "governance": ["typing", "errors"],   # compliance rules only
    "contracts": ["typing", "errors"],    # protocol & interface models
    "events": ["typing", "errors"],       # immutable event MODELS only


    # ================================================================
    # L2 â€” Decision Normalization (Keystone)
    # ================================================================
    # decision:
    #   - does NOT evaluate engines
    #   - does NOT access context, users, tenants
    #   - ONLY merges & normalizes outcomes
    # ================================================================

    "decision": ["typing", "errors"],


    # ================================================================
    # L2 â€” Pure Decision Engines (GAâ€‘Sealed)
    # ================================================================
    # Engines are:
    #   - deterministic
    #   - replayâ€‘safe
    #   - pure (NO IO, NO persistence, NO orchestration)
    #
    # Engines may import ONLY structural utilities.
    # ================================================================

    "rbac": ["typing", "errors"],
    "policy": ["typing", "errors"],
    "quota": ["typing", "errors"],
    "risk": ["typing", "errors"],
    "consent": ["typing", "errors"],
    "audit": ["typing", "errors"],        # explanation ONLY (not logging)


    # ================================================================
    # Registry â€” Static metadata ONLY
    # ================================================================
    # Registry is NOT an engine.
    # It contains names, ordering, invariants â€” never behavior.
    # ================================================================

    "registry": ["kernel", "errors"],
}


# ---------------------------------------------------------------------
# Kernel Absolute Isolation Rules
# ---------------------------------------------------------------------
# Kernel MUST NOT import ANYTHING from afritech.platform.core,
# including errors, typing, or any L1 / L2 module.
# ---------------------------------------------------------------------

KERNEL_FORBIDDEN_IMPORT_ROOTS = {
    "afritech.platform.core",
}


# ---------------------------------------------------------------------
# Forbidden Import Roots (ANYWHERE in core)
# ---------------------------------------------------------------------
# These are MODULE ROOTS (ASTâ€‘enforced).
# Presence indicates immediate GA violation.
# ---------------------------------------------------------------------

FORBIDDEN_IMPORT_ROOTS = {

    # -------------------------------------------------
    # Time / nondeterminism
    # -------------------------------------------------
    "time",
    "datetime",
    "random",

    # -------------------------------------------------
    # Concurrency / async
    # -------------------------------------------------
    "asyncio",
    "threading",
    "multiprocessing",
    "concurrent",

    # -------------------------------------------------
    # IO / system interaction
    # -------------------------------------------------
    "subprocess",
    "socket",
    "os",
    "sys",
    "pathlib",     # allowed in tools/tests ONLY

    # -------------------------------------------------
    # Network / frameworks
    # -------------------------------------------------
    "requests",
    "urllib",
    "http",
    "fastapi",
    "django",
    "flask",

    # -------------------------------------------------
    # Persistence / brokers
    # -------------------------------------------------
    "sqlalchemy",
    "psycopg",
    "sqlite3",
    "redis",
    "kafka",
}


# ---------------------------------------------------------------------
# Forbidden Runtime Patterns
# ---------------------------------------------------------------------
# These are LASTâ€‘RESORT safety nets.
# Exact string matches scanned in source code.
# ---------------------------------------------------------------------

FORBIDDEN_PATTERNS = {

    # -------------------------------------------------
    # Clocks
    # -------------------------------------------------
    "time.time",
    "time.monotonic",
    "datetime.now",
    "datetime.utcnow",
    "datetime.today",

    # -------------------------------------------------
    # Randomness / entropy
    # -------------------------------------------------
    "random.random",
    "random.randint",
    "random.choice",
    "uuid.uuid4",

    # -------------------------------------------------
    # IO / debugging
    # -------------------------------------------------
    "print(",
    "logging.",
}


# ---------------------------------------------------------------------
# Typing Module Special Allowances
# ---------------------------------------------------------------------
# typing MAY validate input and MAY raise ValidationError.
# typing MUST NOT raise any other exception type.
# ---------------------------------------------------------------------

TYPING_ALLOWED_EXCEPTION_NAMES = {
    "ValidationError",
}


# ---------------------------------------------------------------------
# Module Purity Vocabulary Guards
# ---------------------------------------------------------------------
# These are heuristic, caseâ€‘insensitive scans.
# Presence indicates semantic drift.
# ---------------------------------------------------------------------

MODULE_FORBIDDEN_VOCAB = {

    # ================================================================
    # tenancy â€” grammar ONLY
    # ================================================================
    "tenancy": {
        "resolve",
        "resolver",
        "lookup",
        "registry",
        "service",
    },

    # ================================================================
    # identity â€” model ONLY
    # ================================================================
    "identity": {
        "authorize",
        "permission",
        "rbac",
        "policy",
        "service",
        "repository",
    },

    # ================================================================
    # policy â€” condition logic ONLY
    # ================================================================
    "policy": {
        "resolve",
        "lookup",
        "fetch",
        "registry",
        "service",
        "context",
        "tenant",
        "user",
        "rbac",
        "role",
        "permission",
        "quota",
        "feature",
    },

    # ================================================================
    # audit â€” explanation ONLY
    # ================================================================
    "audit": {
        "store",
        "persist",
        "save",
        "write",
        "log",
        "publish",
        "emit",
        "send",
    },

    # ================================================================
    # registry â€” metadata ONLY
    # ================================================================
    "registry": {
        "authorize",
        "decide",
        "evaluate",
        "business",
        "policy",
    },
}


# ---------------------------------------------------------------------
# Golden Rule (documentation-only, enforced by tests)
# ---------------------------------------------------------------------
"""
Each core module must answer ONE question only.

If a module appears to answer more than one:
    â†’ the architecture is already broken.
"""
