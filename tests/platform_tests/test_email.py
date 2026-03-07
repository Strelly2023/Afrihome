from control_plane.governance.identity.identity_invariants import validate_email
import pytest

@pytest.mark.parametrize("ok", [
    "user@example.com", "a.b+c-d_1@sub.domain.co", "x@y.z",
])
def test_email_ok(ok):
    assert validate_email(ok) == ok.lower()

@pytest.mark.parametrize("bad", [
    "", "no-at", "a@b", "user@-bad.com", "user@bad-.com", "user@.nodomain",
])
def test_email_bad(bad):
    with pytest.raises(Exception):
        validate_email(bad)