"""Credential-free container boundary and a minimal stdio MCP execution bridge."""

import argparse
import base64
import json
import os
from pathlib import Path, PurePosixPath
import selectors
import stat
import subprocess
import sys
import tarfile
import tempfile
import time
import uuid

ROOT = Path(__file__).resolve().parents[1]
IMAGE = "rootprint-issue-worker:local"
MAX_PATCH = 4 * 1024 * 1024
REPORT_SCHEMA = {
    "type": "object", "additionalProperties": False,
    "properties": {
        "status": {"type": "string", "enum": ["ready", "needs-information", "blocked", "complete"]},
        "kind": {"type": "string", "enum": ["bug", "feature"]},
        "summary": {"type": "string", "minLength": 1, "maxLength": 12000},
        "contract": {"type": "string", "maxLength": 500},
        "regression": {"type": "string", "maxLength": 4000},
        "duplicates": {"type": "array", "maxItems": 10, "items": {"type": "integer", "minimum": 1}},
    },
    "required": ["status", "kind", "summary", "contract", "regression", "duplicates"],
}


def clean_env():
    # The runtime needs HOME for rootless Podman, but no credentials are forwarded.
    return {k: os.environ[k] for k in ("PATH", "HOME", "XDG_RUNTIME_DIR") if k in os.environ}


def command(args, *, timeout=120, limit=32768):
    """Bound output in memory; never interpolate model input into a host shell."""
    data = bytearray()
    deadline = time.monotonic() + timeout
    with subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=clean_env()) as process:
        with selectors.DefaultSelector() as selector:
            selector.register(process.stdout, selectors.EVENT_READ)
            try:
                while True:
                    if time.monotonic() > deadline:
                        raise subprocess.TimeoutExpired(args, timeout)
                    events = selector.select(timeout=0.2)
                    if not events and process.poll() is not None:
                        break
                    if events:
                        chunk = os.read(process.stdout.fileno(), 8192)
                        if not chunk:
                            break
                        data.extend(chunk[:max(0, limit + 1 - len(data))])
                code = process.wait(timeout=max(0.1, deadline - time.monotonic()))
            except BaseException:
                process.kill()
                process.wait()
                raise
    return code, data[:limit].decode("utf-8", errors="replace"), len(data) > limit


def safe_path(value):
    if (not isinstance(value, str) or not value or "\\" in value
            or any(ord(c) < 32 for c in value)
            or any(p in ("", ".", "..", ".git") for p in value.split("/"))
            or PurePosixPath(value).is_absolute()):
        raise ValueError("Invalid patch path")
    return value


def validate_changes(changes):
    if not isinstance(changes, list) or not 1 <= len(changes) <= 100:
        raise ValueError("Expected 1–100 changed files")
    seen = set()
    size = 0
    for entry in changes:
        if not isinstance(entry, dict) or set(entry) != {"path", "mode", "content"}:
            raise ValueError("Invalid patch entry")
        path = safe_path(entry["path"])
        if path in seen or entry["mode"] not in ("100644", "100755"):
            raise ValueError("Duplicate path or unsupported file mode")
        seen.add(path)
        if entry["content"] is not None:
            data = base64.b64decode(entry["content"], validate=True)
            size += len(data)
            if len(data) > 1024 * 1024 or size > MAX_PATCH:
                raise ValueError("Patch exceeds size limit")
    return changes


def validate_report(report):
    if not isinstance(report, dict) or set(report) != set(REPORT_SCHEMA["required"]):
        raise ValueError("Incomplete phase report")
    for field in ("status", "kind", "summary", "contract", "regression"):
        if not isinstance(report[field], str) or len(report[field]) > REPORT_SCHEMA["properties"][field].get("maxLength", 100):
            raise ValueError("Invalid report field")
    if (report["status"] not in REPORT_SCHEMA["properties"]["status"]["enum"]
            or report["kind"] not in ("bug", "feature") or not report["summary"].strip()
            or not isinstance(report["duplicates"], list) or len(report["duplicates"]) > 10
            or any(type(n) is not int or n < 1 for n in report["duplicates"])):
        raise ValueError("Invalid phase report")
    if report["contract"]:
        safe_path(report["contract"])
    return report


def build(runtime):
    """Send only Git-tracked source, never .git, host caches, or credential files."""
    files = subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT).decode().split("\0")
    with tempfile.TemporaryFile() as context:
        # Gzip magic survives Docker's bounded sniff even when PAX headers come first.
        with tarfile.open(fileobj=context, mode="w:gz") as archive:
            for name in filter(None, files):
                path = PurePosixPath(name)
                if (".opencode" in path.parts or path.name.startswith(".env")
                        or path.suffix in (".pem", ".key")):
                    continue
                archive.add(ROOT / name, arcname=name, recursive=False)
        context.seek(0)
        subprocess.run([runtime, "build", "-t", IMAGE, "-f", "automation/worker.Dockerfile", "-"],
                       stdin=context, env=clean_env(), check=True, timeout=900)


class Sandbox:
    def __init__(self, runtime="docker"):
        self.runtime = runtime
        self.name = "rootprint-worker-" + uuid.uuid4().hex
        self.base = None

    def __enter__(self):
        args = [self.runtime, "run", "--detach", "--name", self.name, "--read-only",
                "--network", "none", "--cap-drop", "ALL", "--security-opt", "no-new-privileges",
                "--pids-limit", "256", "--memory", "4g", "--cpus", "2", "--user", "1000:1000",
                "--tmpfs", "/work:rw,exec,mode=1777,size=3g",
                "--tmpfs", "/tmp:rw,exec,mode=1777,size=1g", IMAGE]
        try:
            code, _, _ = command(args)
            if code:
                raise RuntimeError("Could not start credential-free sandbox")
            init = ("cp -R /seed/. /work/ && cp -R /opt/npm-cache /tmp/npm-cache && mkdir -p /tmp/home && "
                    "git init -q && git add . && "
                    "git -c user.name=Rootprint -c user.email=worker@invalid "
                    "-c core.hooksPath=/dev/null commit -qm baseline && git rev-parse HEAD")
            code, output, _ = self.run(init)
            if code:
                raise RuntimeError("Could not initialize sandbox")
            self.base = output.strip().splitlines()[-1]
            return self
        except Exception:
            self.__exit__(None, None, None)
            raise

    def __exit__(self, *_):
        command([self.runtime, "rm", "--force", self.name], timeout=30)

    def run(self, script, timeout=90):
        if not isinstance(script, str) or len(script) > 16000:
            raise ValueError("Command exceeds limit")
        return command([self.runtime, "exec", "--workdir", "/work", self.name,
                        "/usr/bin/timeout", "--kill-after=2", str(timeout), "/bin/sh", "-c", script],
                       timeout=timeout + 10)

    def changes(self):
        code, output, truncated = command(
            [self.runtime, "exec", "--workdir", "/work", self.name,
             "/usr/bin/python3", "/bridge/worker_sandbox.py", "export", "--base", self.base],
            limit=MAX_PATCH * 2)
        if code or truncated:
            raise RuntimeError("Could not safely export patch")
        return validate_changes(json.loads(output))


def export(base):
    """Runs INSIDE the container. Output is still untrusted on the host."""
    root = Path("/work")
    names = subprocess.check_output(["git", "diff", "--name-only", "-z", base], cwd=root)
    names += subprocess.check_output(["git", "ls-files", "--others", "--exclude-standard", "-z"], cwd=root)
    entries = []
    for name in sorted(set(filter(None, names.decode().split("\0")))):
        safe_path(name)
        file = root / name
        if not file.resolve().is_relative_to(root) or any(p.is_symlink() for p in (file, *file.parents)):
            raise ValueError("Symlink export is forbidden")
        if not file.exists():
            entries.append({"path": name, "mode": "100644", "content": None})
        else:
            mode = file.stat().st_mode
            if not stat.S_ISREG(mode) or file.stat().st_size > 1024 * 1024:
                raise ValueError("Unsupported exported file")
            entries.append({"path": name, "mode": "100755" if mode & 0o111 else "100644",
                            "content": base64.b64encode(file.read_bytes()).decode()})
    print(json.dumps(validate_changes(entries)))


def mcp_response(request, sandbox, result_path):
    method = request.get("method")
    if method == "initialize":
        return {"protocolVersion": "2024-11-05", "capabilities": {"tools": {}},
                "serverInfo": {"name": "rootprint-sandbox", "version": "1"}}
    if method == "ping":
        return {}
    if method == "tools/list":
        return {"tools": [
            {"name": "run", "description": "Run a shell command in the offline credential-free /work sandbox (90s limit).",
             "inputSchema": {"type": "object", "properties": {"command": {"type": "string", "maxLength": 16000}},
                             "required": ["command"], "additionalProperties": False}},
            {"name": "report", "description": "Submit the structured phase result exactly once.", "inputSchema": REPORT_SCHEMA},
        ]}
    if method == "tools/call":
        params = request["params"]
        if params["name"] == "run" and set(params["arguments"]) == {"command"}:
            code, output, truncated = sandbox.run(params["arguments"]["command"])
            text = json.dumps({"exitCode": code, "output": output, "truncated": truncated})
        elif params["name"] == "report":
            report = validate_report(params["arguments"])
            with result_path.open("x", encoding="utf-8") as result:
                json.dump(report, result)
            text = "Phase report recorded. End this session."
        else:
            raise ValueError("Unknown tool or arguments")
        return {"content": [{"type": "text", "text": text}]}
    raise ValueError("Unsupported MCP method")


def serve(runtime, container, result):
    sandbox = Sandbox(runtime)
    # Never create or select a container from model-supplied tool arguments.
    sandbox.name = container
    for line in sys.stdin:
        request = json.loads(line)
        if "id" not in request:
            continue
        response = {"jsonrpc": "2.0", "id": request["id"]}
        try:
            response["result"] = mcp_response(request, sandbox, Path(result))
        except Exception:
            response["error"] = {"code": -32602, "message": "Sandbox tool rejected request or execution failed"}
        print(json.dumps(response), flush=True)


def smoke(runtime):
    with Sandbox(runtime) as sandbox:
        probe = """python3 - <<'PY'
import os, pathlib, socket
assert not any(k in os.environ for k in ('OPENAI_API_KEY', 'GITHUB_TOKEN', 'IMPLEMENTATION_APP_PRIVATE_KEY'))
assert not pathlib.Path('/var/run/docker.sock').exists()
assert not pathlib.Path('/run/podman/podman.sock').exists()
assert pathlib.Path('/proc/self/status').read_text().split('CapEff:')[1].split()[0] == '0000000000000000'
try:
    pathlib.Path('/bridge/worker_sandbox.py').write_text('tampered')
except OSError:
    pass
else:
    raise AssertionError('writable trusted bridge')
try:
    socket.create_connection(('1.1.1.1', 443), timeout=1)
except OSError:
    pass
else:
    raise AssertionError('network access')
pathlib.Path('sandbox-probe.txt').write_text('credential-free')
PY"""
        code, output, _ = sandbox.run(probe)
        if code:
            raise RuntimeError("Sandbox isolation probe failed: " + output)
        assert sandbox.changes() == [{"path": "sandbox-probe.txt", "mode": "100644",
                                      "content": base64.b64encode(b"credential-free").decode()}]
        # A malicious output file must not turn into a host read or a Git blob.
        sandbox.run("ln -s /etc/passwd stolen.txt")
        try:
            sandbox.changes()
        except RuntimeError:
            pass
        else:
            raise AssertionError("Symlink export was accepted")
    print("Sandbox isolation and hostile-artifact probes passed")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["build", "smoke", "mcp", "export"])
    parser.add_argument("--runtime", choices=["docker", "podman"], default="docker")
    parser.add_argument("--container")
    parser.add_argument("--result")
    parser.add_argument("--base")
    args = parser.parse_args()
    if args.mode == "build":
        build(args.runtime)
    elif args.mode == "smoke":
        smoke(args.runtime)
    elif args.mode == "export":
        export(args.base)
    else:
        serve(args.runtime, args.container, args.result)
