## Local workflow

```bash
# format & auto-fix simple issues
ruff check . --fix && black .

# run tests (quiet)
pytest -q

# architecture hard gate (report -> arch_report.json)
python tools/check_architecture.py --root . --format json --fail-under 10 > arch_report.json