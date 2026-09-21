"""Shared helpers for subprocess-based CLI qualification tests."""

import os
from pathlib import Path
import subprocess
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE = REPO_ROOT / "src"


def cli_environment() -> dict[str, str]:
    """Return a subprocess environment that can run `python -m docsprout`.

    Inside the source checkout the suite injects `src` into the in-process
    path only; make the same resolution visible to subprocesses. When the
    package is installed, subprocesses use the installed module.
    """
    env = dict(os.environ)
    if str(SOURCE) in sys.path:
        existing = env.get("PYTHONPATH")
        env["PYTHONPATH"] = str(SOURCE) if not existing else f"{SOURCE}{os.pathsep}{existing}"
    return env


def run_cli(root: Path, *arguments: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        [sys.executable, "-m", "docsprout", *arguments, "--root", str(root)],
        cwd=str(root), capture_output=True, text=True, encoding="utf-8",
        env=cli_environment(), timeout=90,
    )
    if check and result.returncode != 0:
        raise AssertionError(
            f"docsprout {arguments} failed with {result.returncode}:\n"
            f"--- stdout ---\n{result.stdout}\n--- stderr ---\n{result.stderr}"
        )
    return result
