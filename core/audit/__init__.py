"""
GA Enterprise Core — Audit Spine (Deterministic)
-----------------------------------------------

LAYER: L2

Purpose:
- Immutable audit records
- Deterministic content hashing
- Chain hashing (prev + record)
- Merkle root calculator
- Store protocol (no IO)
- Pure audit writer (no background behavior)
"""

from .audit_record import AuditRecord
from .audit_writer import write_audit_entry
from .chain import ZERO_HASH, ChainLink, make_chain_link
from .merkle import merkle_root
from .storage_protocol import AuditStore

__all__ = [
    "AuditRecord",
    "ChainLink",
    "ZERO_HASH",
    "make_chain_link",
    "merkle_root",
    "AuditStore",
    "write_audit_entry",
]
