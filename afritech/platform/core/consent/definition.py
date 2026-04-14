from __future__ import annotations

"""
GA Enterprise Core â€” Consent Definition
--------------------------------------

LAYER: L2 (Pure Engine)
Dependencies: core.consent.grammar + core.errors.base + stdlib
Deterministic: YES
Side effects: NONE
IO / Time / Network: NONE

Purpose:
- Represent an immutable consent requirement definition
- Declare what consent is required for an action to be legal

Rules:
- Pure value object only
- No kernel dependencies
- No evaluation, persistence, or time access
- Structural invariants MUST raise ValidationError
"""

from dataclasses import dataclass
from typing import Tuple

from afritech.platform.core.consent.grammar import (
    validate_consent_scope,
    validate_legal_basis,
)
from afritech.platform.core.errors.base import ValidationError


# ============================================================
# Consent Definition (pure value object)
# ============================================================

@dataclass(frozen=True, slots=True)
class ConsentDefinition:
    """
    Immutable consent requirement definition.

    Attributes:
        consent_id:
            Logical identifier of the consent requirement
            (e.g. "user-marketing-consent").
        scopes:
            Tuple of consent scopes this definition applies to
            (e.g. ("marketing",)).
        legal_bases:
            Tuple of acceptable legal bases under which processing
            is permitted (e.g. ("consent", "legitimate_interest")).
        required:
            Whether consent is strictly required, or optional
            (used by higher layers to handle soft restrictions).
    """

    consent_id: str
    scopes: Tuple[str, ...]
    legal_bases: Tuple[str, ...]
    required: bool = True

    def __post_init__(self) -> None:
        # ----------------------------------------------------
        # Structural validation
        # ----------------------------------------------------

        if not isinstance(self.consent_id, str) or not self.consent_id.strip():
            raise ValidationError(
                "consent_id must be a non-empty string",
                metadata={"consent_id": self.consent_id},
            )

        if not isinstance(self.required, bool):
            raise ValidationError(
                "required must be a boolean",
                metadata={"required": self.required},
            )

        # ----------------------------------------------------
        # Scope validation (grammar-authoritative)
        # ----------------------------------------------------

        if not isinstance(self.scopes, tuple):
            raise ValidationError(
                "scopes must be a tuple",
                metadata={"scopes_type": type(self.scopes).__name__},
            )

        if not self.scopes:
            raise ValidationError(
                "scopes must contain at least one scope",
                metadata={"scopes": self.scopes},
            )

        validated_scopes = tuple(
            validate_consent_scope(scope) for scope in self.scopes
        )
        object.__setattr__(self, "scopes", validated_scopes)

        # ----------------------------------------------------
        # Legal basis validation (grammar-authoritative)
        # ----------------------------------------------------

        if not isinstance(self.legal_bases, tuple):
            raise ValidationError(
                "legal_bases must be a tuple",
                metadata={
                    "legal_bases_type":
                        type(self.legal_bases).__name__
                },
            )

        if not self.legal_bases:
            raise ValidationError(
                "legal_bases must contain at least one legal basis",
                metadata={"legal_bases": self.legal_bases},
            )

        validated_bases = tuple(
            validate_legal_basis(basis) for basis in self.legal_bases
        )
        object.__setattr__(self, "legal_bases", validated_bases)


# ============================================================
# Consent Definition ABI (explicit, frozen)
# ============================================================

__all__ = [
    "ConsentDefinition",
]
