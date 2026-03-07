
from core.rbac import *
from core.typing import RoleName, Permission, UserId


def test_permission_matching():
    assert permission_matches('inventory.read', 'inventory.read')
    assert permission_matches('inventory.*', 'inventory.read')
    assert not permission_matches('inventory.read', 'inventory.item.read')
    assert permission_matches('inventory.**', 'inventory.item.read')
    assert not permission_matches('*.read', 'inventory.item.read')


def test_deny_wins_across_roles():
    reader = Role(name=RoleName('reader'), allow=('inventory.read',), deny=())
    writer = Role(name=RoleName('writer'), allow=('inventory.write',), deny=('inventory.*',))
    policy = Policy(roles={str(reader.name): reader, str(writer.name): writer})

    subject = Subject(user_id=UserId('u1'), roles=(reader.name, writer.name))
    dec = evaluate(policy, subject, Permission('inventory.read'))
    assert dec.allowed is False
    assert dec.reason.startswith('deny:')


def test_allow_when_no_deny_and_allow_matches():
    reader = Role(name=RoleName('reader'), allow=('inventory.read',), deny=())
    policy = Policy(roles={str(reader.name): reader})
    subject = Subject(user_id=None, roles=(reader.name,))
    dec = evaluate(policy, subject, Permission('inventory.read'))
    assert dec.allowed is True


def test_default_deny():
    reader = Role(name=RoleName('reader'), allow=('inventory.read',), deny=())
    policy = Policy(roles={str(reader.name): reader})
    subject = Subject(user_id=None, roles=(reader.name,))
    dec = evaluate(policy, subject, Permission('inventory.write'))
    assert dec.allowed is False
    assert dec.reason == 'deny: default'
