from __future__ import annotations
#afritech/platform/core/identity/identity_invariants.py
"""
GA Enterprise Core â€” Identity Invariants (Deterministic)
-------------------------------------------------------

LAYER: L1 (Foundation)
Dependencies: stdlib + core.errors
Deterministic: YES
Side effects: NONE
IO / Network: NONE

Purpose:
- Enforce strict, deterministic identity validation rules
- Provide reusable invariants for identity governance
- Remain suitable for core usage and pure testing

GA v1 Notes:
- Identity invariants apply to User-based identity
- ValidationError is raised for backward compatibility
- Email validation is syntactic only (RFC-inspired, not RFC-complete)
"""



import re

from afritech.platform.core.errors import ValidationError


__all__ = [
    "validate_email",
    "normalize_display_name",
]


# ---------------------------------------------------------------------------
# Email validation
# ---------------------------------------------------------------------------
#
# Constraints:
# - ASCII only
# - No whitespace
# - Requires at least one dot in domain
# - TLD must be alphabetic (1â€“63 chars)
# - Max length 254 (practical limit used by most systems)
#
# This is intentionally stricter than RFC 5322 to avoid ambiguity
# and keep behavior deterministic across systems.
#
_EMAIL_RE = re.compile(
    r"^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@"      # local part
    r"(?:[A-Za-z0-9]"                          # domain label start
    r"(?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?\.)+"  # middle labels + dots
    r"[A-Za-z]{1,63}$"                         # TLD
)


def validate_email(email: str) -> str:
    """
    Validate and normalize an email address.

    Rules:
    - Must be a string
    - Must be non-empty after trimming
    - Must be ASCII-only and syntactically valid
    - Length <= 254 characters

    Returns:
        Normalized (lowercased, stripped) email string.

    Raises:
        ValidationError: if the email violates invariants.
    """
    if not isinstance(email, str):
        raise ValidationError("Email must be a string")

    normalized = email.strip()
    if not normalized:
        raise ValidationError("Email cannot be empty")

    if len(normalized) > 254:
        raise ValidationError("Email is too long")

    if not _EMAIL_RE.fullmatch(normalized):
        raise ValidationError("Invalid email format")

    # Normalization rule:
    # - Lowercase entire address to avoid ambiguity
    #   (acceptable and common in modern systems)
    return normalized.lower()


# ---------------------------------------------------------------------------
# Display name normalization
# ---------------------------------------------------------------------------

def normalize_display_name(name: str) -> str:
    """
    Normalize and validate a human-readable display name.

    Rules:
    - Must be a string
    - Must be non-empty after trimming
    - Max length: 200 characters
    - No character restrictions (international-friendly)

    Returns:
        Trimmed display name.

    Raises:
        ValidationError: if the name violates invariants.
    """
    if not isinstance(name, str):
        raise ValidationError("Display name must be a string")

    normalized = name.strip()
    if not normalized:
        raise ValidationError("Display name cannot be empty")

    if len(normalized) > 200:
        raise ValidationError("Display name is too long")

    return normalized
