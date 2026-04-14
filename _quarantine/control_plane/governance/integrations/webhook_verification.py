from dataclasses import dataclass
from enum import Enum, auto
from typing import Tuple, Optional
import re

from core.errors import InvariantViolationError


# ---------- Grammar helpers ----------

#_HEADER_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")  # canonical lower-case header
#_PATH_RE = re.compile(r"^/[-a-zA-Z0-9._~/]*$")    # conservative path grammar
_HEADER_RE = re.compile(r'^[a-z0-9][a-z0-9-]*$')  # canonical lower-case header
_PATH_RE = re.compile(r'^/[-a-zA-Z0-9._~/]*$')    # conservative path grammar


def normalize_header_name(name: str) -> str:
    if not isinstance(name, str):
        raise InvariantViolationError("header name must be a string")
    n = name.strip().lower()
    if not _HEADER_RE.match(n):
        raise InvariantViolationError(f"Invalid header name: {name!r}")
    return n


def normalize_path(path: str) -> str:
    if not isinstance(path, str):
        raise InvariantViolationError("path must be a string")
    p = path.strip()
    if not p.startswith("/"):
        p = "/" + p
    if not _PATH_RE.match(p):
        raise InvariantViolationError(f"Invalid path: {path!r}")
    return p


# ---------- Enums (declarative only; no crypto here) ----------

class HttpMethod(Enum):
    GET = auto()
    POST = auto()
    PUT = auto()
    DELETE = auto()
    PATCH = auto()


class SignatureAlgorithm(Enum):
    """
    Declarative signature algorithms for webhook verification.

    NOTE: Governance-only. Application/infra will implement crypto.
    """
    HMAC_SHA256 = auto()
    HMAC_SHA512 = auto()
    RSA_SHA256 = auto()
    ED25519 = auto()


@dataclass(frozen=True, slots=True)
class WebhookVerification:
    """
    Immutable webhook verification policy (governance-only).

    Fields
    ------
    provider_key           : which provider this policy belongs to
    path                   : URL path where webhook is received (no server binding here)
    methods                : allowed HTTP methods
    signature_header       : name of header carrying signature (normalized)
    timestamp_header       : optional header for timestamp-based replay protection
    algorithm              : declared SignatureAlgorithm (no crypto here)
    secret_ref             : opaque reference to secret location (no secret material)
    tolerance_ms           : replay tolerance window (>= 0)
    scheme_prefix          : optional prefix in header value (e.g., "v1=")
    required_headers       : optional extra headers that MUST be present (normalized)
    description            : optional human note
    """
    provider_key: str
    path: str
    methods: Tuple[HttpMethod, ...]
    signature_header: str
    algorithm: SignatureAlgorithm
    secret_ref: str

    timestamp_header: Optional[str] = None
    tolerance_ms: int = 0
    scheme_prefix: Optional[str] = None
    required_headers: Tuple[str, ...] = ()
    description: str = ""

    def __post_init__(self) -> None:
        # provider_key: reuse provider key grammar from provider_config (duplicated to keep this module standalone)
        _KEY_RE = re.compile(r"^[a-z][a-z0-9]*(?:[._-][a-z0-9]+)*$")
        if not isinstance(self.provider_key, str):
            raise InvariantViolationError("provider_key must be a string")
        pk = self.provider_key.strip().lower()
        if not _KEY_RE.match(pk):
            raise InvariantViolationError(f"Invalid provider_key: {self.provider_key!r}")
        object.__setattr__(self, "provider_key", pk)

        p = normalize_path(self.path)
        object.__setattr__(self, "path", p)

        if not self.methods:
            raise InvariantViolationError("methods cannot be empty")
        object.__setattr__(self, "methods", tuple(self.methods))

        sh = normalize_header_name(self.signature_header)
        object.__setattr__(self, "signature_header", sh)

        if self.timestamp_header is not None:
            th = normalize_header_name(self.timestamp_header)
            object.__setattr__(self, "timestamp_header", th)

        tol = int(self.tolerance_ms)
        if tol < 0:
            raise InvariantViolationError("tolerance_ms must be >= 0")
        object.__setattr__(self, "tolerance_ms", tol)

        if self.scheme_prefix is not None and not isinstance(self.scheme_prefix, str):
            raise InvariantViolationError("scheme_prefix must be a string or None")

        if any(not isinstance(h, str) for h in self.required_headers):
            raise InvariantViolationError("required_headers must be Tuple[str, ...]")
        object.__setattr__(self, "required_headers", tuple(normalize_header_name(h) for h in self.required_headers))

        if not isinstance(self.secret_ref, str) or not self.secret_ref.strip():
            raise InvariantViolationError("secret_ref must be a non-empty string (opaque reference)")