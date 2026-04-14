# Determinism

The system is deterministic by law.

Given:
- The same engine inputs
- The same evaluation order (or any order)
- The same enum definitions

The output `Decision` is guaranteed identical.

All nondeterminism is explicitly forbidden:
- No time
- No randomness
- No IO
- No external state