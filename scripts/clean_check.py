"""Reproduce setup in a disposable source copy; optionally prove mutation detection."""

import argparse
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import venv

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mutations", action="store_true")
    args = parser.parse_args()
    npm = shutil.which("npm") or "npm"
    node = shutil.which("node") or "node"
    with tempfile.TemporaryDirectory(prefix="xmerkle-clean-") as temporary:
        target = Path(temporary)
        ignore = shutil.ignore_patterns("node_modules", "dist", "build", "__pycache__", "*.egg-info")
        for directory in ["packages", "conformance", "scripts", "openspec", "docs", ".github"]:
            shutil.copytree(ROOT / directory, target / directory, ignore=ignore)
        for file in ["package.json", "package-lock.json", "requirements-dev.txt", "README.md", "AGENTS.md", ".gitignore"]:
            shutil.copy2(ROOT / file, target / file)

        def run(*command):
            subprocess.run(command, cwd=target, check=True)

        run(npm, "ci", "--ignore-scripts")
        environment = target / ".venv"
        venv.EnvBuilder(with_pip=True).create(environment)
        python = str(environment / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python"))
        run(python, "-m", "pip", "install", "-r", "requirements-dev.txt")
        run(python, "scripts/check.py")
        run(python, "scripts/package_check.py")
        if args.mutations:
            source = target / "packages/typescript/src/index.ts"
            original = source.read_text(encoding="utf-8")
            mutations = [
                ('encode(canonicalize(representation))', 'encode(canonicalize(representation) + " ")', 1),
                ('children.push(node(', 'children.unshift(node(', 1),
                ('Math.min(16, full.length)', 'Math.min(15, full.length)', 4),
            ]
            for before, after, failing_case in mutations:
                assert original.count(before) == 1
                source.write_text(original.replace(before, after), encoding="utf-8")
                run(npm, "run", "build")
                result = subprocess.run([node, "--test", "--test-reporter=tap", "packages/typescript/test/conformance.test.mjs"],
                                        cwd=target, capture_output=True, text=True)
                assert result.returncode != 0 and f"not ok {failing_case} -" in result.stdout, result.stdout + result.stderr
                print(f"Detected intentional mutation: {before}")
    print("Clean-source install, verification, and package checks passed")


if __name__ == "__main__":
    main()
