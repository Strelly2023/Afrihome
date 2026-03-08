"""
GA Enterprise Core — Execution Layer

LAYER: L1

Purpose:
- Deterministic execution boundary
- Strict write enforcement
- Logical transaction model
"""

from .execution_context import ExecutionContext
from .strict_write import StrictWriteMode
from .transaction import TransactionBoundary

__all__ = [
    "ExecutionContext",
    "StrictWriteMode",
    "TransactionBoundary",
]
