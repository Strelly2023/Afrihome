import subprocess
import sys
from pathlib import Path


def run_runtime_checker(path: Path) -> subprocess.CompletedProcess:
    """
    Run the AfriTech runtime mutation checker with scope
    restricted to the given path (file or directory).

    This matches CI behavior but allows isolated fixture testing.
    """
    return subprocess.run(
        [sys.executable, "tools/check_runtime_mutation.py"],
        cwd=path if path.is_dir() else path.parent,
        capture_output=True,
        text=True,
    )