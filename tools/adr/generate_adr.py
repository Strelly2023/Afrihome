from pathlib import Path
import sys
import yaml 

TEMPLATES = yaml.safe_load(
    Path("constitution/adr_templates.yml").read_text()
)

HEADER = """# {adr_id} — {title}

| Field | Value |
|------|------|
| Status | Draft |
| Class | {class_name} |
| ADR ID | {adr_id} |
| Constitutional Level | {level} |
| Breaking Change | No |
| Requires Migration | No |
| Enforced By Tests | ❌ |
"""

def generate(class_code: str, number: int, title: str) -> None:
    if class_code not in TEMPLATES["classes"]:
        raise SystemExit(f"❌ Unknown ADR class: {class_code}")

    spec = TEMPLATES["classes"][class_code]
    adr_id = f"ADR-{class_code}-{number:03d}"

    content = HEADER.format(
        adr_id=adr_id,
        title=title,
        class_name=spec["name"],
        level=spec["level"],
    )

    for section in spec["required_sections"]:
        content += f"\n## {section}\n\n"

    path = Path(f"docs/decisions/{adr_id}.md")
    if path.exists():
        raise SystemExit(f"❌ ADR already exists: {path}")

    path.write_text(content)
    print(f"✅ Created {path}")


if __name__ == "__main__":
    generate(sys.argv[1], int(sys.argv[2]), sys.argv[3])