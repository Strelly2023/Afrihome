import re

from core.errors import ValidationError

# Simple, strict, deterministic email validation (no I/O, no DNS lookups)
'''_EMAIL_RE = re.compile(
    r"^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@"
    r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?"
    r"(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?)*$"
)'''
_EMAIL_RE = re.compile(
    r'^[A-Za-z0-9.!#$%&\'*+/=?^_`{|}~-]+@'
    r'[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?'
    r'(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?)*$'
)

def validate_email(email: str) -> str:
    if not isinstance(email, str):
        raise ValidationError("Email must be a string")
    e = email.strip()
    if not e or len(e) > 254 or not _EMAIL_RE.match(e):
        raise ValidationError("Invalid email format")
    return e.lower()


def normalize_display_name(name: str) -> str:
    if not isinstance(name, str):
        raise ValidationError("Display name must be a string")
    n = name.strip()
    if not n:
        raise ValidationError("Display name cannot be empty")
    if len(n) > 200:
        raise ValidationError("Display name is too long")
    return n