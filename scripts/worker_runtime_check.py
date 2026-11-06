"""Optional Linux container/OpenCode checks; no GitHub or provider credential needed."""

import argparse

from worker_agent import preflight
from worker_sandbox import Sandbox, smoke


def main(runtime):
    smoke(runtime)
    with Sandbox(runtime) as sandbox:
        preflight(sandbox)
        code, output, _ = sandbox.run("python3 scripts/check.py && python3 scripts/package_check.py", timeout=300)
        if code:
            raise RuntimeError("Offline baseline verification failed:\n" + output)
    print("OpenCode config, real MCP startup, and offline integrated/package checks passed")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runtime", choices=["docker", "podman"], default="docker")
    main(parser.parse_args().runtime)
