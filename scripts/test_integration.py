"""Cross-language acceptance checks, including command-line trust boundaries."""

from datetime import datetime, timezone
import json
import os
from pathlib import Path
import random
import shutil
import subprocess
import sys
import tempfile
import unittest

from rootprint import hash_json, hash_value

ROOT = Path(__file__).resolve().parents[1]
NODE = shutil.which("node") or "node"
VECTORS = json.loads((ROOT / "conformance/v1/vectors.json").read_text(encoding="utf-8"))


def cli_checks(test, commands):
    """Same checks work with source CLIs and installed package CLIs."""
    for command in commands:
        for vector in VECTORS["valid"]:
            result = subprocess.run(command, input=vector["json"].encode("utf-8"), capture_output=True, check=True)
            record = json.loads(result.stdout)
            test.assertEqual(record["digest"], vector["digest"])
            test.assertEqual(record["algorithm"], "sha256")
            test.assertEqual(record["protocol"], "rootprint-v1")
            timestamp = datetime.fromisoformat(record["calculatedAt"].replace("Z", "+00:00"))
            test.assertEqual(record["label"], f"{timestamp:%Y%m%d_%H%M%S}-sha256-v1-{record['digest'][:16]}")
            test.assertEqual(result.stderr, b"")
        for raw in [text.encode("utf-8") for text in VECTORS["invalid"]] + [b'"\xff"', b'"\xc0\xaf"']:
            result = subprocess.run(command, input=raw, capture_output=True)
            test.assertNotEqual(result.returncode, 0, raw)
            test.assertEqual(result.stdout, b"")
            test.assertTrue(result.stderr)
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "data with spaces.json"
            path.write_text('{"b":2,"a":1}', encoding="utf-8")
            result = subprocess.run([*command, "--prefix-length", "24", str(path)], capture_output=True, check=True)
            record = json.loads(result.stdout)
            test.assertEqual(record["digest"], hash_value({"a": 1, "b": 2})["digest"])
            test.assertEqual(record["label"].split("-")[-1], record["digest"][:24])
        for arguments in [["--prefix-length", "0"], ["--prefix-length", "1.5"], ["--prefix-length", "65"], ["--unknown"]]:
            result = subprocess.run([*command, *arguments], input=b"null", capture_output=True)
            test.assertNotEqual(result.returncode, 0)
            test.assertEqual(result.stdout, b"")


class Integration(unittest.TestCase):
    def test_source_clis(self):
        cli_checks(self, [[NODE, str(ROOT / "packages/typescript/dist/cli.js")], [sys.executable, "-m", "rootprint"]])

    def test_fixed_clock_records_and_generated_nested_inputs(self):
        rng = random.Random(803)

        def value(depth):
            if depth == 0:
                return rng.choice([None, False, True, 0, -0.0, 1e30, 5e-324, "😀", "é", "\n"])
            if rng.randrange(2):
                return [value(depth - 1) for _ in range(rng.randrange(4))]
            return {key: value(depth - 1) for key in rng.sample(["a", "😀", "\ue000", "__proto__", "0"], rng.randrange(5))}

        sources = [vector["json"] for vector in VECTORS["valid"]]
        sources += [json.dumps(value(4), ensure_ascii=False) for _ in range(80)]
        module = (ROOT / "packages/typescript/dist/index.js").as_uri()
        program = f'''
          import {{hashJson}} from {json.dumps(module)};
          import {{readFileSync}} from "node:fs";
          const sources = JSON.parse(readFileSync(0,"utf8"));
          console.log(JSON.stringify(sources.map(s => hashJson(s, {{clock: () => new Date("2026-11-02T09:04:05.987Z")}}))));
        '''
        expected = [hash_json(source, clock=lambda: datetime(2026, 11, 2, 9, 4, 5, 987000, tzinfo=timezone.utc)) for source in sources]
        for zone in ["UTC", "America/Los_Angeles", "Asia/Tokyo"]:
            result = subprocess.run([NODE, "--input-type=module", "-e", program], input=json.dumps(sources).encode(),
                                    env={**os.environ, "TZ": zone}, capture_output=True, check=True)
            self.assertEqual(json.loads(result.stdout), expected)


if __name__ == "__main__":
    unittest.main()
