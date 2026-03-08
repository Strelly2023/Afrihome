# control_plane/governance/identity/identity_invariants.py
from __future__ import annotations

import re
from typing import Final

from core.errors import ValidationError

# -----------------------------
# User ID normalization (optional, keep here for single authority)
# Grammar: start with a letter, then letters/digits/._-
# -----------------------------
_USER_ID_RE: Final[re.Pattern[str]] = re.compile(r"^[a-z][a-z0-9._-]*$")


def normalize_user_id(raw: str) -> str:
    """
    Trim + lowercase + grammar check.

    NOTE: This is intentionally minimal and deterministic. It is not a global
    identity naming policy; it is the governance grammar authority.
    """
    if not isinstance(raw, str):
        raise ValidationError("user_id must be a string")
    uid = raw.strip().lower()
    if not uid:
        raise ValidationError("user_id must not be empty")
    if not _USER_ID_RE.match(uid):
        raise ValidationError(f"Invalid user_id: {raw!r}")
    return uid


# -----------------------------
# Email validation (deterministic, no DNS/IO)
# - Local part: commonly used ASCII set (simplified)
# - Domain: labels 1..63 chars, no leading/trailing hyphen, at least one dot
# - TLD: 1..63 letters (allows single-letter TLD like 'x@y.z')
# -----------------------------
_LABEL = r"(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?)"
_EMAIL_RE: Final[re.Pattern[str]] = re.compile(
    r"^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@"  # local part (ASCII subset)
    rf"(?:{_LABEL}\.)+"  # one or more labels followed by a dot
    r"[A-Za-z]{1,63}$"  # TLD (1..63 letters)
)


def validate_email(email: str) -> str:
    """
    Validate an email address deterministically:
    - Must be a string
    - Total length <= 254
    - Matches the _EMAIL_RE pattern above
    Returns the normalized (lowercased) email on success.
    """
    if not isinstance(email, str):
        raise ValidationError("Email must be a string")
    e = email.strip()
    if not e or len(e) > 254 or not _EMAIL_RE.match(e):
        raise ValidationError("Invalid email format")
    return e.lower()


# -----------------------------
# Display name normalization
# -----------------------------
def normalize_display_name(name: str) -> str:
    """
    Normalize and validate a display name:
    - Must be a string
    - Non-empty after trimming
    - Max length 200
    Returns the trimmed name on success.
    """
    if not isinstance(name, str):
        raise ValidationError("Display name must be a string")
    n = name.strip()
    if not n:
        raise ValidationError("Display name cannot be empty")
    if len(n) > 200:
        raise ValidationError("Display name is too long")
    return n


__all__ = [
    "normalize_user_id",
    "validate_email",
    "normalize_display_name",
]
