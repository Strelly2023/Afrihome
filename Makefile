.PHONY: lint fmt test arch ci

# Run static analysis
lint:
    ruff check .

# Auto‑format the code
fmt:
    ruff check . --fix
    black .

# Run tests
test:
    pytest -q

# Generate architecture report (uses your existing script)
arch:
    python tools/check_architecture.py --root . --format json --fail-under 10 > arch_report.json

# CI pipeline (lint + test + arch)
ci: arch lint test
