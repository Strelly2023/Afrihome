from pathlib import Path
from validate_adr_traceability import (
    collect_adrs,
    extract_adrs_from_tests,
)

OUTPUT = Path("docs/generated/adr_coverage.md")


def generate():
    adrs = collect_adrs(Path("docs/decisions"))
    coverage = extract_adrs_from_tests(Path("tests"))

    lines = ["# ADR Coverage Report\n"]

    for adr in sorted(adrs):
        lines.append(f"## {adr}")

        if adr in coverage:
            lines.append("✔ Covered by:")
            for f in sorted(coverage[adr]):
                lines.append(f"- {f}")
        else:
            lines.append("❌ NOT COVERED")

        lines.append("")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text("\n".join(lines))


if __name__ == "__main__":
    generate()