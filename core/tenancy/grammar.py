"""
GA Enterprise Core — Tenancy Slug Grammar
-----------------------------------------

LAYER: L3
Dependencies: core.errors (L0)
Deterministic: YES
IO: NONE
RBAC: FORBIDDEN
"""

import re
from typing import Final

from core.errors import GrammarViolationError

TENANT_SLUG_PATTERN: Final[re.Pattern[str]] = re.compile(r"^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$")


def normalize_tenant_slug(slug: str) -> str:
    if slug is None:
        raise GrammarViolationError("Tenant slug must not be None")
    return slug.strip().lower()


def is_valid_tenant_slug(slug: str) -> bool:
    s = normalize_tenant_slug(slug)
    return bool(TENANT_SLUG_PATTERN.match(s))


def validate_tenant_slug(slug: str) -> str:
    s = normalize_tenant_slug(slug)
    if not TENANT_SLUG_PATTERN.match(s):
        raise GrammarViolationError(f"Invalid tenant slug: {slug!r}")
    return s
