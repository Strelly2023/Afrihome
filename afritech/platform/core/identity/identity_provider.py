"""
GA Enterprise Core â€” Identity Provider
-------------------------------------

LAYER: L1 (Foundation)
Dependencies: stdlib only
Deterministic: YES
Side effects: NONE

Purpose:
- Represent how a User authenticated in GA v1

GA v1 Rules:
- IdentityProvider describes HOW authentication occurred
- It does NOT represent identity kind or actor type
- In GA v1, Identity == User

IMPORTANT:
- Do NOT branch authorization logic on IdentityProvider
- Identity kind (USER / SERVICE / SYSTEM) is introduced in GA v2
- This enum is safe to persist and expose via external APIs
"""

from enum import Enum


class IdentityProvider(str, Enum):
    """
    Authentication provider used during identity verification.

    Values:
    - PASSWORD â†’ username/password authentication
    - OAUTH    â†’ external identity provider (Google, Azure AD, etc.)
    - API_KEY  â†’ API key acting on behalf of a user
    - SYSTEM   â†’ platform-initiated or internal system action
    """

    PASSWORD = "password"
    OAUTH = "oauth"
    API_KEY = "api_key"
    SYSTEM = "system"
