"""Activation reporting must not mistake the presence of credentials for readiness."""

import json
import os
import subprocess
import sys
import unittest
from unittest.mock import patch

import activation


class Activation(unittest.TestCase):
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
