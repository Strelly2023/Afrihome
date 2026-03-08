"""
GA Enterprise Core — Outbox Topic Grammar
-----------------------------------------

LAYER: L2
Dependencies: core.errors (L0)
Deterministic: YES
IO: NONE
"""

import re
from typing import Final

from core.errors import GrammarViolationError

# segments like "foo.bar.baz"; each segment: [a-z][a-z0-9]*
TOPIC_PATTERN: Final[re.Pattern[str]] = re.compile(r'^[a-z][a-z0-9]*(?:\.[a-z][a-z0-9]*)*$')

def normalize_topic(topic: str) -> str:
    if topic is None:
        raise GrammarViolationError("Topic must not be None")
    t = topic.strip().lower()
    return t

def is_valid_topic(topic: str) -> bool:
    t = normalize_topic(topic)
    return bool(TOPIC_PATTERN.match(t))

def validate_topic(topic: str) -> str:
    t = normalize_topic(topic)
    if not TOPIC_PATTERN.match(t):
        raise GrammarViolationError(f"Invalid topic: {topic!r}")
    return t