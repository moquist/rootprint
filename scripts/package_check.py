"""Build both distributions, install them in temporary environments, exercise CLIs."""

import json
from email.parser import BytesParser
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
import tempfile
import tomllib
import unittest
import venv
import zipfile

from test_integration import ROOT, cli_checks


def main():
    npm = shutil.which("npm") or "npm"
    subprocess.run([npm, "run", "build"], cwd=ROOT, check=True)
    version = tomllib.loads((ROOT / "packages/python/pyproject.toml").read_text(encoding="utf-8"))["project"]["version"]
    assert json.loads((ROOT / "packages/typescript/package.json").read_text(encoding="utf-8"))["version"] == version
    license_text = (ROOT / "LICENSE").read_bytes()
    subprocess.run([sys.executable, "-m", "build", "packages/python"], cwd=ROOT, check=True)
    with tempfile.TemporaryDirectory(prefix="rootprint-packages-") as temporary:
        folder = Path(temporary)
        result = subprocess.run([npm, "pack", "--ignore-scripts", "--workspace", "packages/typescript", "--pack-destination", temporary, "--json"],
                                cwd=ROOT, check=True, capture_output=True, text=True)
        package = folder / json.loads(result.stdout)[0]["filename"]
        with tarfile.open(package) as archive:
            assert archive.extractfile("package/LICENSE").read() == license_text
            assert json.load(archive.extractfile("package/package.json"))["license"] == "EPL-2.0"
            assert archive.extractfile("package/src/index.ts").read() == (ROOT / "packages/typescript/src/index.ts").read_bytes()
        with tarfile.open(ROOT / f"packages/python/dist/rootprint-{version}.tar.gz") as archive:
            assert archive.extractfile(f"rootprint-{version}/LICENSE").read() == license_text
        subprocess.run([npm, "install", "--ignore-scripts", "--prefix", temporary, str(package)], check=True)
        pyenv = folder / "pyenv"
        venv.EnvBuilder(with_pip=True).create(pyenv)
        python = pyenv / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")
        wheel = ROOT / f"packages/python/dist/rootprint-{version}-py3-none-any.whl"
        with zipfile.ZipFile(wheel) as archive:
            assert archive.read(f"rootprint-{version}.dist-info/licenses/LICENSE") == license_text
            metadata = BytesParser().parsebytes(archive.read(f"rootprint-{version}.dist-info/METADATA"))
            assert metadata["License-Expression"] == "EPL-2.0"
            assert archive.read("rootprint/__init__.py") == (ROOT / "packages/python/src/rootprint/__init__.py").read_bytes()
        subprocess.run([str(python), "-m", "pip", "install", str(wheel)], check=True)
        cli_checks(unittest.TestCase(), [
            [str(folder / "node_modules/.bin" / ("rootprint.cmd" if sys.platform == "win32" else "rootprint"))],
            [str(pyenv / ("Scripts/rootprint.exe" if sys.platform == "win32" else "bin/rootprint"))],
        ])
        # Execute documented API examples against the installed packages.
        subprocess.run([str(python), "-c", 'from rootprint import hash_value, hash_json, digest; r=hash_value({"b":2,"a":1}); assert hash_json(\'{"a":1,"b":2}\')["digest"] == r["digest"] == digest({"a":1,"b":2})'], cwd=folder, check=True)
        subprocess.run([shutil.which("node") or "node", "--input-type=module", "-e", 'import {hash,hashJson,digest} from "rootprint"; const r=hash({b:2,a:1}); if(hashJson(\'{"a":1,"b":2}\').digest !== r.digest || digest({a:1,b:2}) !== r.digest) throw Error("example failed");'], cwd=folder, check=True)
    print("Both installed packages passed CLI and documented API checks")


if __name__ == "__main__":
    main()
