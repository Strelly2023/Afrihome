
from core.guards import TokenBucketPolicy, TokenBucketState, try_consume
from core.typing import UnixMillis


def test_token_bucket():
    pol = TokenBucketPolicy(capacity=5, refill_rate_per_ms=0.001)
    s0 = TokenBucketState(tokens=0.0, last_refill_ms=UnixMillis(0))
    s1, allowed = try_consume(s0, UnixMillis(0), pol)
    assert allowed is False
    s2, allowed = try_consume(s1, UnixMillis(2000), pol)
    assert allowed is True
    s3, allowed = try_consume(s2, UnixMillis(2000), pol)
    assert allowed is True
