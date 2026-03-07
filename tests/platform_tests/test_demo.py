import re

GOOD = [
    "a", "a1", "a.b", "a-b", "a_b", "abc.def-ghi_jkl",
]
BAD = [
    "", ".", "-a", "_a", "a.", "a..b", "A", "a..", "a__b", "a--b", "a.-b",
]

KEY = re.compile(r'^[a-z][a-z0-9]*(?:[._-][a-z0-9]+)*$')

def test_key_regex_good():
    for k in GOOD:
        assert KEY.fullmatch(k), k

def test_key_regex_bad():
    for k in BAD:
        assert not KEY.fullmatch(k), k