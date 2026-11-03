"""Build both distributions, install them in temporary environments, exercise CLIs."""

import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import tomllib
import unittest
import venv

from test_integration import ROOT, cli_checks


def main():
    npm = shutil.which("npm") or "npm"
    subprocess.run([npm, "run", "build"], cwd=ROOT, check=True)
    version = tomllib.loads((ROOT / "packages/python/pyproject.toml").read_text(encoding="utf-8"))["project"]["version"]
    assert json.loads((ROOT / "packages/typescript/package.json").read_text(encoding="utf-8"))["version"] == version
    subprocess.run([sys.executable, "-m", "build", "packages/python"], cwd=ROOT, check=True)
    with tempfile.TemporaryDirectory(prefix="xmerkle-packages-") as temporary:
        folder = Path(temporary)
        result = subprocess.run([npm, "pack", "--ignore-scripts", "--workspace", "packages/typescript", "--pack-destination", temporary, "--json"],
                                cwd=ROOT, check=True, capture_output=True, text=True)
        package = folder / json.loads(result.stdout)[0]["filename"]
        subprocess.run([npm, "install", "--ignore-scripts", "--prefix", temporary, str(package)], check=True)
        pyenv = folder / "pyenv"
        venv.EnvBuilder(with_pip=True).create(pyenv)
        python = pyenv / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")
        wheel = ROOT / f"packages/python/dist/xmerkle-{version}-py3-none-any.whl"
        subprocess.run([str(python), "-m", "pip", "install", str(wheel)], check=True)
        cli_checks(unittest.TestCase(), [
            [str(folder / "node_modules/.bin" / ("xmerkle.cmd" if sys.platform == "win32" else "xmerkle"))],
            [str(pyenv / ("Scripts/xmerkle.exe" if sys.platform == "win32" else "bin/xmerkle"))],
        ])
        # Execute documented API examples against the installed packages.
        subprocess.run([str(python), "-c", 'from xmerkle import hash_value, hash_json, digest; r=hash_value({"b":2,"a":1}); assert hash_json(\'{"a":1,"b":2}\')["digest"] == r["digest"] == digest({"a":1,"b":2})'], cwd=folder, check=True)
        subprocess.run([shutil.which("node") or "node", "--input-type=module", "-e", 'import {hash,hashJson,digest} from "xmerkle"; const r=hash({b:2,a:1}); if(hashJson(\'{"a":1,"b":2}\').digest !== r.digest || digest({a:1,b:2}) !== r.digest) throw Error("example failed");'], cwd=folder, check=True)
    print("Both installed packages passed CLI and documented API checks")


if __name__ == "__main__":
    main()
