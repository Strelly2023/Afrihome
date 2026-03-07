
from core.audit import AuditRecord, write_audit_entry, merkle_root
from core.audit.chain import ZERO_HASH
from core.typing import UnixMillis, TenantId


class MemoryAuditStore:
    def __init__(self):
        self.links = []
    def append_link(self, link):
        self.links.append(link)
    def last_link(self):
        return self.links[-1] if self.links else None
    def get_range(self, start_index: int, limit: int):
        return self.links[start_index:start_index+limit]


def test_audit_record_hash_and_chain():
    store = MemoryAuditStore()

    r1 = AuditRecord.create(
        ts=UnixMillis(100), category='user', action='created', tenant_id=TenantId('t1'),
        principal='u1', event_id=None, data={'name': 'A'}
    )
    l1 = write_audit_entry(store, r1)

    r2 = AuditRecord.create(
        ts=UnixMillis(150), category='user', action='updated', tenant_id=TenantId('t1'),
        principal='u1', event_id=None, data={'name': 'B'}
    )
    l2 = write_audit_entry(store, r2)

    assert l1.index == 0 and l2.index == 1
    assert l2.prev_hash == l1.chain_hash
    root = merkle_root([l1.record_hash, l2.record_hash])
    assert isinstance(root, str) and len(root) == 64
