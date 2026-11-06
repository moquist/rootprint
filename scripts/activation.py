"""Report verified local facts and remaining remote activation requirements.

This is deliberately not a self-attestation flag: credentials in the environment
do not prove a GitHub ruleset, worker isolation, or a successful issue-to-merge run.
"""

import argparse
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def status():
    remote = subprocess.run(["git", "remote", "get-url", "origin"], cwd=ROOT,
                            capture_output=True, text=True)
    has_remote = remote.returncode == 0 and bool(remote.stdout.strip())
    blockers = []
    if not has_remote:
        blockers.append("No origin remote: GitHub event-driven automation and hosted checks are unavailable")
    blockers.extend([
        "Initial hosted CI success is owner-reported; recorded latest-revision matrix/run evidence remains pending",
        "Scoped GitHub App installation and OpenAI provider access have not been live-verified",
        "Issue worker is implemented and disabled by default; hosted isolation and issue-to-PR acceptance are unverified",
        "Independent reviewer is implemented and disabled by default; hosted App attribution and no-bypass merge gates are unverified",
        "Controlled issue-to-PR-to-review-to-merge acceptance run is pending",
        "Automatic version PRs and verified publishing integration are not implemented or verified",
        "Registry ownership and publishing identity are not verified",
    ])
    if not (ROOT / "LICENSE").is_file():
        blockers.append("Project license has not been selected")
    return {
        "mode": "local",
        "githubMaintenanceActive": False,
        "publishingActive": False,
        "originConfigured": has_remote,
        "prepared": ["OpenSpec contract", "local verification", "read-only CI workflow", "issue forms",
                     "dependency update configuration", "isolated OpenCode issue worker (manual merges)",
                     "tool-free current-head independent reviewer"],
        "blockers": blockers,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--require-active", action="store_true", help="Exit nonzero while automation is inactive")
    args = parser.parse_args()
    report = status()
    print(json.dumps(report, indent=2))
    raise SystemExit(1 if args.require_active and not report["githubMaintenanceActive"] else 0)
