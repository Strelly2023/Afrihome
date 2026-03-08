import re
from core.errors import ValidationError

# Strict, deterministic email validator (no DNS/IO).
# - Local part: common ASCII set (simplified)
# - Domain: labels 1..63 chars, no leading/trailing hyphen, at least one dot
# - TLD: 1..63 letters (allows single-letter TLD like "x@y.z")
_LABEL = r"(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?)"
_EMAIL_RE = re.compile(
    r"^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@"  # local part
    rf"(?:{_LABEL}\.)+"                    # one or more labels followed by a dot
    r"[A-Za-z]{1,63}$"                     # TLD (1..63 letters)
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