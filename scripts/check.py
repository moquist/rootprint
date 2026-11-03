"""Run integrated local verification with this Python interpreter."""

import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
OPENSPEC = ROOT / "node_modules" / ".bin" / ("openspec.cmd" if sys.platform == "win32" else "openspec")


def run(*args):
    subprocess.run(args, cwd=ROOT, check=True)


if __name__ == "__main__":
    run(shutil.which("npm") or "npm", "run", "check")
    run(sys.executable, "-m", "unittest", "discover", "-s", "packages/python/tests")
    run(sys.executable, "-m", "unittest", "discover", "-s", "scripts", "-p", "test_*.py")
    run(sys.executable, "-m", "ruff", "check", "packages/python", "scripts")
    run(str(OPENSPEC), "validate", "--all", "--strict")
