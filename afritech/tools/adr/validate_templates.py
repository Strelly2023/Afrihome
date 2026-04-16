import re
import sys
import yaml
from pathlib import Path

TEMPLATES = yaml.safe_load(
    Path("constitution/adr_templates.yml").read_text()
)

ADR_ID_PATTERN = re.compile(r"ADR-([A-Z]{2})-\d{3}")

def validate_file(path: Path):
    content = path.read_text()

    match = ADR_ID_PATTERN.match(path.stem)
    if not match:
        return False, "Invalid ADR filename"

    class_code = match.group(1)

    if class_code not in TEMPLATES["classes"]:
        return False, f"Unknown ADR class: {class_code}"

    spec = TEMPLATES["classes"][class_code]

    for section in spec["required_sections"]:
        if f"## {section}" not in content:
            return False, f"Missing section: {section}"

    for term in spec["forbidden_terms"]:
        if term.lower() in content.lower():
            return False, f"Forbidden term used: '{term}'"

    return True, None


def main():
    errors = False
    for file in Path("docs/decisions").glob("ADR-*.md"):
        ok, err = validate_file(file)
        if not ok:
            print(f"❌ {file.name}: {err}")
            errors = True
        else:
            print(f"✅ {file.name}")

    if errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
