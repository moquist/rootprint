"""Activation reporting must not mistake the presence of credentials for readiness."""

import json
import os
import subprocess
import sys
import unittest
from unittest.mock import patch

import activation


class Activation(unittest.TestCase):
    def test_recorded_hosted_evidence_is_not_a_live_activation_claim(self):
        for returncode in (0, 2):
            with patch(
                "activation.subprocess.run",
                return_value=subprocess.CompletedProcess([], returncode, "origin" if returncode == 0 else ""),
            ) as run:
                report = activation.status()
            self.assertEqual(report["originConfigured"], returncode == 0)
            self.assertFalse(report["liveRemoteChecksPerformed"])
            self.assertFalse(report["githubMaintenanceActive"])
            self.assertFalse(report["publishingActive"])
            evidence = report["recordedHostedEvidence"]
            self.assertEqual(evidence["repository"], "moquist/rootprint")
            self.assertEqual(evidence["asOf"], "2026-11-07")
            self.assertEqual(evidence["ci"], "https://github.com/moquist/rootprint/actions/runs/42332002332")
            self.assertEqual(evidence["independentReview"],
                             "https://github.com/moquist/rootprint/actions/runs/42332000613")
            self.assertEqual(evidence["manualIssueLifecycle"],
                             "https://github.com/moquist/rootprint/issues/12#issuecomment-6688011714")
            self.assertEqual(evidence["mergeRules"], "https://github.com/moquist/rootprint/rules/26673301")
            blockers = " ".join(report["blockers"])
            self.assertNotIn("owner-reported", blockers)
            self.assertNotIn("App attribution and no-bypass merge gates are unverified", blockers)
            self.assertIn("Automatic rebase merging", blockers)
            self.assertIn("adversarial", blockers)
            self.assertEqual("No origin remote configured for this checkout" in report["blockers"],
                             returncode != 0)
            run.assert_called_once_with(["git", "remote", "get-url", "origin"], cwd=activation.ROOT,
                                        capture_output=True, text=True)

    def test_configured_origin_does_not_claim_remote_gates_are_active(self):
        secret_url = "https://private-token@example.invalid/owner/repo"
        with patch("activation.subprocess.run", return_value=subprocess.CompletedProcess([], 0, secret_url)):
            report = activation.status()
        self.assertTrue(report["originConfigured"])
        self.assertFalse(report["githubMaintenanceActive"])
        self.assertFalse(report["publishingActive"])
        self.assertNotIn(secret_url, json.dumps(report))

    def test_require_active_fails_without_verified_integrations(self):
        result = subprocess.run([sys.executable, str(activation.ROOT / "scripts/activation.py"), "--require-active"],
                                env={**os.environ, "GITHUB_TOKEN": "fake-do-not-print", "OPENAI_API_KEY": "fake-do-not-print"},
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertFalse(json.loads(result.stdout)["githubMaintenanceActive"])
        self.assertNotIn("fake-do-not-print", result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
