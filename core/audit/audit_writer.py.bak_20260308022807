
"""
GA Enterprise Core — Audit Writer
---------------------------------

LAYER: L2
Dependencies:
- core.audit.audit_record
- core.audit.chain
- core.audit.storage_protocol
- core.kernel.invariants

Rules:
- No IO
- Deterministic hashing
- Pure state transitions
"""


from core.audit.audit_record import AuditRecord
from core.audit.chain import ChainLink, make_chain_link
from core.audit.storage_protocol import AuditStore
from core.kernel.invariants import assert_not_none


def write_audit_entry(store: AuditStore, record: AuditRecord) -> ChainLink:
    assert_not_none(store, "store")
    assert_not_none(record, "record")
    prev = store.last_link()
    link = make_chain_link(prev, record.content_hash)
    store.append_link(link)
    return link
