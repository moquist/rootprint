"""Build context must survive Docker's 1024-byte archive sniff, including PAX paths."""

import io
import os
from pathlib import Path
import tarfile
import tempfile
import unittest
from unittest.mock import patch

import worker_sandbox


class BuildContext(unittest.TestCase):
    def test_bounded_archive_probe_and_filtered_contents_for_both_runtimes(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            long_path = "src/" + "x" * 120 + ".txt"
            included = {long_path: b"long-name source", "automation/worker.Dockerfile": b"FROM scratch\nCOPY . .\n"}
            excluded = {".opencode/private.md": b"private config", "private/.env.local": b"environment secret",
                        "private/key.pem": b"PEM secret", "private/key.key": b"key secret"}
            for name, content in {**included, **excluded, ".git/config": b"git credential", "cache.txt": b"host cache"}.items():
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(content)
            tracked = "\0".join([*included, *excluded]) + "\0"

            for runtime in ("docker", "podman"):
                def accept_build(args, *, stdin, env, check, timeout):
                    self.assertEqual(args, [runtime, "build", "-t", worker_sandbox.IMAGE,
                                            "-f", "automation/worker.Dockerfile", "-"])
                    self.assertTrue(check)
                    self.assertEqual(timeout, 900)
                    self.assertFalse(set(env) - {"PATH", "HOME", "XDG_RUNTIME_DIR"})
                    prefix = stdin.read(1024)
                    # BuildKit recognizes gzip magic; otherwise it tries the first
                    # tar member within Buildx's peek. PAX needs a following header.
                    if not prefix.startswith(b"\x1f\x8b\x08"):
                        with tarfile.open(fileobj=io.BytesIO(prefix), mode="r:") as probe:
                            self.assertIsNotNone(probe.next())
                    stdin.seek(0)
                    with tarfile.open(fileobj=stdin, mode="r:*") as archive:
                        self.assertEqual(set(archive.getnames()), set(included))
                        for name, content in included.items():
                            self.assertEqual(archive.extractfile(name).read(), content)

                with self.subTest(runtime=runtime), patch.object(worker_sandbox, "ROOT", root), \
                        patch("worker_sandbox.subprocess.check_output", return_value=tracked.encode()) as files, \
                        patch("worker_sandbox.subprocess.run", side_effect=accept_build) as command, \
                        patch.dict(os.environ, {"OPENAI_API_KEY": "fake-provider-secret", "GITHUB_TOKEN": "fake-github-secret"}):
                    worker_sandbox.build(runtime)
                files.assert_called_once_with(["git", "ls-files", "-z"], cwd=root)
                command.assert_called_once()


if __name__ == "__main__":
    unittest.main()
