"""Report local facts, recorded hosted evidence, and remaining activation work.

Recorded evidence is historical and repository-specific, not a live health probe.
Credentials in the environment do not establish autonomous maintenance readiness.
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
        blockers.append("No origin remote configured for this checkout")
    blockers.extend([
        "Current GitHub settings, App installations, provider access and runner isolation are not live-probed by this report",
        "Hosted adversarial input, repeated events, exhausted attempts/recovery and failure deduplication acceptance remains incomplete",
        "Controlled bug-to-failing-regression-to-fix acceptance remains pending; issue #12 exercised a documentation change",
        "Automatic rebase merging is not implemented or verified; last inspected repository setting had auto-merge disabled",
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
        "liveRemoteChecksPerformed": False,
        # Historical observations from docs/local-work.md, independent of this checkout's origin.
        "recordedHostedEvidence": {
            "repository": "moquist/rootprint",
            "asOf": "2026-11-07",
            "ledger": "docs/local-work.md",
            "ci": "https://github.com/moquist/rootprint/actions/runs/42332002332",
            "independentReview": "https://github.com/moquist/rootprint/actions/runs/42332000613",
            "manualIssueLifecycle": "https://github.com/moquist/rootprint/issues/12#issuecomment-6688011714",
            "mergeRules": "https://github.com/moquist/rootprint/rules/26673301",
        },
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
