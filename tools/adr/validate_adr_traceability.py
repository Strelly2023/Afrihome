import re
import sys
from pathlib import Path

ADR_PATTERN = re.compile(r"ADR-[A-Z]{2}-\d{3}")


# ---------------------------------------------------------
# 1. Collect ADRs from docs
# ---------------------------------------------------------

def collect_adrs(adr_dir: Path):
    adrs = set()

    for file in adr_dir.glob("ADR-*.md"):
        match = ADR_PATTERN.search(file.name)
        if match:
            adrs.add(match.group())

    return adrs


# ---------------------------------------------------------
# 2. Extract ADR references from tests
# ---------------------------------------------------------

def extract_adrs_from_tests(test_dir: Path):
    coverage = {}

    for file in test_dir.rglob("test_*.py"):
        content = file.read_text()

        matches = ADR_PATTERN.findall(content)

        for adr in matches:
            coverage.setdefault(adr, set()).add(str(file))

    return coverage


# ---------------------------------------------------------
# 3. Validation
# ---------------------------------------------------------

def validate(adrs, coverage):
    errors = False

    # ❌ ADR with no tests
    uncovered = [adr for adr in adrs if adr not in coverage]

    if uncovered:
        print("\n❌ ADRs without test coverage:")
        for adr in uncovered:
            print(f"  - {adr}")
        errors = True

    # ❌ Tests referencing unknown ADRs
    unknown = [adr for adr in coverage if adr not in adrs]

    if unknown:
        print("\n❌ Unknown ADR references in tests:")
        for adr in unknown:
            print(f"  - {adr}")
        errors = True

    # ✅ Report coverage
    print("\n📊 ADR Coverage:")
    for adr in sorted(coverage):
        print(f"{adr}:")
        for f in sorted(coverage[adr]):
            print(f"  - {f}")

    return errors


# ---------------------------------------------------------
# Entry
# ---------------------------------------------------------

def main():
    adr_dir = Path("docs/decisions")
    test_dir = Path("tests")

    adrs = collect_adrs(adr_dir)
    coverage = extract_adrs_from_tests(test_dir)

    errors = validate(adrs, coverage)

    if errors:
        sys.exit(1)


if __name__ == "__main__":
    main()