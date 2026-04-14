from __future__ import annotations

"""
GA Enterprise Core â€” Risk Grammar
--------------------------------

LAYER: L2 (Pure Engine)
Dependencies: stdlib + core.errors.base
Deterministic: YES
Side effects: NONE
IO / Time / Network: NONE

Purpose:
- Define canonical grammar for risk signals, score ranges, and bands
- Centralize validation for risk definitions
- Ensure deterministic, replay-safe risk semantics

Rules:
- Grammar ONLY (no evaluation, no persistence)
- No kernel imports
- No L1 foundation imports (except CoreError types)
- Uses primitive types exclusively
- Grammar violations MUST raise GrammarViolationError
"""

from typing import Final

from afritech.platform.core.errors.base import GrammarViolationError


# ============================================================
# Canonical risk signals
# ============================================================

# Signals represent *inputs* to risk scoring.
# They are symbolic and interpreted only by the evaluation engine.
#
# Examples:
# - geo_mismatch
# - velocity_spike
# - anomaly_detected
# - sensitive_action
SIGNALS: Final[set[str]] = {
    "geo_mismatch",
    "velocity_spike",
    "anomaly_detected",
    "sensitive_action",
    "untrusted_device",
    "ip_reputation",
}


# ============================================================
# Risk score range
# ============================================================

# Risk score is an integer in a fixed range.
# The scale itself is arbitrary but must be stable.
SCORE_MIN: Final[int] = 0
SCORE_MAX: Final[int] = 100


# ============================================================
# Canonical risk bands
# ============================================================

# Bands represent coarse groupings of scores.
BANDS: Final[set[str]] = {
    "low",
    "medium",
    "high",
    "critical",
}


# ============================================================
# Validation helpers (pure)
# ============================================================

def validate_signal(signal: str) -> str:
    """
    Validate a risk signal name.

    Returns:
        The normalized signal if valid.

    Raises:
        GrammarViolationError if the signal is invalid or unsupported.
    """
    if not isinstance(signal, str) or not signal.strip():
        raise GrammarViolationError(
            "Risk signal must be a non-empty string",
            metadata={"signal": signal},
        )

    value = signal.strip()

    if value not in SIGNALS:
        raise GrammarViolationError(
            "Unsupported risk signal",
            metadata={
                "signal": value,
                "supported": sorted(SIGNALS),
            },
        )

    return value


def validate_score(score: int) -> int:
    """
    Validate a risk score.

    Returns:
        The score if valid.

    Raises:
        GrammarViolationError if the score is invalid or out of range.
    """
    if not isinstance(score, int):
        raise GrammarViolationError(
            "Risk score must be an integer",
            metadata={"score": score},
        )

    if score < SCORE_MIN or score > SCORE_MAX:
        raise GrammarViolationError(
            "Risk score out of range",
            metadata={
                "score": score,
                "min": SCORE_MIN,
                "max": SCORE_MAX,
            },
        )

    return score


def validate_band(band: str) -> str:
    """
    Validate a risk band.

    Returns:
        The normalized band if valid.

    Raises:
        GrammarViolationError if the band is invalid or unsupported.
    """
    if not isinstance(band, str) or not band.strip():
        raise GrammarViolationError(
            "Risk band must be a non-empty string",
            metadata={"band": band},
        )

    value = band.strip()

    if value not in BANDS:
        raise GrammarViolationError(
            "Unsupported risk band",
            metadata={
                "band": value,
                "supported": sorted(BANDS),
            },
        )

    return value


# ============================================================
# Risk Grammar ABI (explicit, frozen)
# ============================================================

__all__ = [
    # Grammar sets
    "SIGNALS",
    "SCORE_MIN",
    "SCORE_MAX",
    "BANDS",

    # Validators
    "validate_signal",
    "validate_score",
    "validate_band",
]
