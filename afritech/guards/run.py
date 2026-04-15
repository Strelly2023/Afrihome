from pathlib import Path
import subprocess

LEGACY_TOOLS = [
    "tools/check_future_imports.py",
    "tools/check_import_boundaries.py",
    "tools/check_global_mutable_state.py",
    "tools/check_runtime_mutation.py",
]

def run_legacy_tool(tool: str):
    print(f"⚠️  Skipping legacy tool (out of scope): {tool}")

def main():
    print("🏛 AfriTech Constitutional Guard Runner")
    print("ℹ Legacy tools are present but excluded by scope")

    for tool in LEGACY_TOOLS:
        run_legacy_tool(tool)

if __name__ == "__main__":
    main()