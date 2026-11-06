"""Exercise lifecycle/recovery and hostile-input boundaries without live credentials."""

import base64
import copy
import json
import os
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from issue_worker import ApiError, MARKER, Worker, discover, load_state, revision, track_ci_failure
from worker_agent import MODEL, config, preflight
from worker_sandbox import MAX_PATCH, mcp_response, validate_changes


def report(status="ready", **fields):
    return {"status": status, "kind": "bug", "summary": "Existing contract violation",
            "contract": "openspec/changes/bootstrap-rootprint-ecosystem/specs/json-merkle/spec.md",
            "regression": "python3 regression.py", "duplicates": [], **fields}


class FakeGitHub:
    repo = "owner/repo"

    def __init__(self, ready=False):
        self.issue = {"number": 7, "title": "Parser bug", "body": "Reproduction", "state": "open",
                      "labels": [{"name": "ready" if ready else "triage"}]}
        self.comments = []
        self.calls = []
        self.prs = []
        self.ref_exists = False
        self.merged = False
        self.failed = False
        self.permission = "read"

    def pages(self, path):
        if path == "/issues/7/comments":
            return copy.deepcopy(self.comments)
        if path.startswith("/issues?"):
            return [copy.deepcopy(self.issue)]
        return []

    def api(self, method, path, data=None):
        self.calls.append((method, path, data))
        if method == "GET":
            if path == "/issues/7":
                return copy.deepcopy(self.issue)
            if path.startswith("/collaborators/"):
                return {"permission": self.permission}
            if path.startswith("/pulls?"):
                return copy.deepcopy(self.prs)
            if path == "/pulls/9":
                return {"number": 9, "html_url": "https://github.com/owner/repo/pull/9", "merged": self.merged,
                        "state": "closed" if self.merged else "open", "head": {"sha": "a" * 40}}
            if "/check-runs?" in path:
                return {"check_runs": [{"name": "ci", "conclusion": "failure" if self.failed else "success"}]}
            if path.endswith("/status"):
                return {"statuses": []}
            if path.startswith("/git/commits/"):
                return {"tree": {"sha": "base-tree"}}
            if path.startswith("/git/ref/"):
                return {"object": {"sha": "new-commit"}}
            if path == "":
                return {"default_branch": "main"}
        if method == "POST":
            if path == "/issues/7/comments":
                comment = {"id": 100, "body": data["body"], "user": {"login": "worker[bot]", "type": "Bot"}}
                self.comments.append(comment)
                return comment
            if path == "/issues/7/labels":
                for label in data["labels"]:
                    if label not in {item["name"] for item in self.issue["labels"]}:
                        self.issue["labels"].append({"name": label})
                return []
            if path in ("/git/blobs", "/git/trees", "/git/commits"):
                return {"sha": "new-commit"}
            if path == "/git/refs":
                if self.ref_exists:
                    raise ApiError(422)
                self.ref_exists = True
                return {}
            if path == "/pulls":
                pr = {"number": 9, "html_url": "https://github.com/owner/repo/pull/9",
                      "head": {"sha": "new-commit", "repo": {"full_name": self.repo}}, "base": {"ref": "main"}}
                self.prs.append(pr)
                return pr
        if method == "PATCH" and path == "/issues/comments/100":
            self.comments[0]["body"] = data["body"]
            return self.comments[0]
        if method == "DELETE" and "/labels/" in path:
            self.issue["labels"] = [label for label in self.issue["labels"] if label["name"] != path.split("/")[-1]]
            return None
        raise AssertionError((method, path, data))

    def state(self):
        return load_state(self.comments, "worker[bot]")[0]


class FakeSandbox:
    runtime, name, base = "docker", "fixed-container", "b" * 40

    def __init__(self, runtime="docker"):
        self.runtime = runtime

    def __enter__(self):
        self.regressions = 0
        return self

    def __exit__(self, *_):
        pass

    def run(self, script, timeout=90):
        if script == "python3 regression.py":
            self.regressions += 1
            return (1 if self.regressions == 1 else 0), "regression evidence", False
        return 0, "verified", False

    def changes(self):
        return [{"path": "packages/python/src/rootprint/__init__.py", "mode": "100644",
                 "content": base64.b64encode(b"fixed").decode()}]


class Lifecycle(unittest.TestCase):
    def worker(self, client):
        return Worker(client, "worker[bot]", 7)

    @patch("issue_worker.Sandbox", FakeSandbox)
    def test_missing_information_and_duplicates_pause_without_repeat_jobs(self):
        for answer, expected in [(report("needs-information", summary="Which input fails?"), "needs-information"),
                                 (report(duplicates=[3], summary="Same reproduction as #3"), "blocked")]:
            client = FakeGitHub()
            with patch("issue_worker.phase", return_value=answer) as model:
                self.worker(client).execute()
                self.worker(client).execute()
            self.assertEqual(model.call_count, 1)
            self.assertEqual(client.state()["status"], expected)
            self.assertEqual(len(client.comments), 1)
            self.assertIn(answer["summary"], client.comments[0]["body"])

    @patch("issue_worker.Sandbox", FakeSandbox)
    def test_ready_issue_to_pr_checks_and_manual_merge_outcome(self):
        client = FakeGitHub(ready=True)
        phases = [report(), report(), report("complete"), report("complete")]
        with patch("issue_worker.phase", side_effect=phases) as model:
            self.worker(client).execute()
        self.assertEqual([c.args[1] for c in model.call_args_list], ["triage", "plan", "implement", "complete"])
        self.assertEqual(client.state()["pr"], 9)
        self.assertEqual(client.state()["status"], "in-progress")
        self.assertEqual(list(client.state()["attempts"].values()), [1])
        pr_body = next(c[2]["body"] for c in client.calls if c[:2] == ("POST", "/pulls"))
        self.assertIn("Before fix (exit 1)", pr_body)
        self.assertIn("Closes #7", pr_body)
        self.assertFalse(any("/merge" in c[1] for c in client.calls))
        client.failed = True
        self.worker(client).execute()
        self.assertEqual(client.state()["status"], "blocked")
        self.assertIn("Failing current-head checks: ci", client.comments[0]["body"])
        self.assertEqual(len(client.comments), 1)
        client.merged = True
        self.worker(client).execute()
        self.assertEqual(client.state()["status"], "done")

    @patch("issue_worker.Sandbox", FakeSandbox)
    def test_passing_before_fix_regression_blocks_implementation_and_publication(self):
        client = FakeGitHub(ready=True)
        with patch("issue_worker.phase", side_effect=[report(), report()]) as model, \
                patch.object(FakeSandbox, "run", return_value=(0, "not failing", False)):
            with self.assertRaises(RuntimeError):
                self.worker(client).execute()
        self.assertEqual(model.call_count, 2)
        self.assertFalse(client.prs)
        self.assertIn("Regression check did not fail", client.state()["message"])

    @patch("issue_worker.Sandbox", FakeSandbox)
    def test_issue_edit_during_implementation_prevents_stale_publication(self):
        client = FakeGitHub(ready=True)

        def model(sandbox, name, context, deadline):
            if name == "complete":
                client.issue["body"] += " Changed requirement"
            return report("complete" if name in ("implement", "complete") else "ready")

        with patch("issue_worker.phase", side_effect=model):
            self.worker(client).execute()
        self.assertFalse(client.prs)
        self.assertEqual(client.state()["status"], "blocked")
        self.assertIn("Issue changed", client.state()["message"])

    @patch("issue_worker.Sandbox", FakeSandbox)
    def test_attempt_limit_survives_reopen_and_requires_authorized_retry(self):
        client = FakeGitHub(ready=True)
        with patch("issue_worker.phase", side_effect=RuntimeError("Provider connection unavailable")) as model:
            for _ in range(3):
                client.issue["labels"].append({"name": "ready"})
                with self.assertRaises(RuntimeError):
                    self.worker(client).execute()
            client.issue["state"] = "closed"
            self.worker(client).execute()
            client.issue["state"] = "open"
            client.issue["labels"].append({"name": "ready"})
            self.worker(client).execute()
            self.assertEqual(model.call_count, 3)
        state = client.state()
        self.assertEqual(list(state["attempts"].values()), [3])
        self.assertEqual(len(state["runs"]), 3)
        client.comments.append({"id": 101, "body": "/rootprint retry", "user": {"login": "visitor", "type": "User"}})
        self.assertFalse(self.worker(client).retry_request())
        client.permission = "write"
        worker = self.worker(client)
        self.assertTrue(worker.retry_request())
        worker.save("ready", "Authorized retry")
        self.assertFalse(self.worker(client).retry_request())
        self.assertEqual(list(client.state()["attempts"].values()), [0])

    @patch("issue_worker.Sandbox", FakeSandbox)
    def test_interrupted_attempt_is_reconciled_and_partial_publication_is_recovered(self):
        client = FakeGitHub(ready=True)
        worker = self.worker(client)
        worker.state["attempts"][worker.rev] = 1
        worker.save("in-progress", "Attempt interrupted")
        with patch("issue_worker.phase", side_effect=[report(), report(), report("complete"), report("complete")]):
            self.worker(client).execute()
        self.assertEqual(list(client.state()["attempts"].values()), [2])
        # Simulate losing the PR-create response before saving its number.
        worker = self.worker(client)
        del worker.state["pr"]
        worker.save("in-progress", "Lost response")
        with patch("issue_worker.phase") as model:
            self.worker(client).execute()
        self.assertFalse(model.called)
        self.assertEqual(len(client.prs), 1)
        self.assertEqual(client.state()["pr"], 9)

    def test_state_spoofing_and_unchanged_events_cannot_reset_attempts(self):
        client = FakeGitHub()
        original = revision(client.issue, [])
        client.comments.append({"id": 1, "body": MARKER + '{"attempts":{}}\n-->',
                                "user": {"login": "attacker", "type": "User"}})
        self.assertEqual(load_state(client.comments, "worker[bot]"), ({}, None))
        client.comments[0]["user"] = {"login": "other[bot]", "type": "Bot"}
        self.assertEqual(revision(client.issue, client.comments), original)
        client.issue["labels"] = [{"name": "ready"}]
        self.assertEqual(revision(client.issue, client.comments), original)
        client.issue["body"] += " New reproduction"
        self.assertNotEqual(revision(client.issue, client.comments), original)


class Boundaries(unittest.TestCase):
    def test_disconnected_bridge_fails_preflight(self):
        sandbox = FakeSandbox()
        for status in ("sandbox disconnected", "✓ sandbox \x1b[90mconnected"):
            outputs = [SimpleNamespace(stdout=json.dumps(config(sandbox, Path("/unused")))),
                       SimpleNamespace(stdout=status), SimpleNamespace(stdout=MODEL)]
            with patch("worker_agent.subprocess.run", side_effect=outputs):
                if "disconnected" in status:
                    with self.assertRaises(RuntimeError):
                        preflight(sandbox)
                else:
                    preflight(sandbox)

    def test_hostile_patch_paths_modes_and_sizes_are_rejected(self):
        for path in ["/etc/passwd", "../secret", "a/../../secret", ".git/config", "x\\..\\secret", "a//b", "a\nb"]:
            with self.subTest(path=path), self.assertRaises(ValueError):
                validate_changes([{"path": path, "mode": "100644", "content": "YQ=="}])
        for entries in [
            [{"path": "link", "mode": "120000", "content": "YQ=="}],
            [{"path": "large", "mode": "100644", "content": base64.b64encode(b"x" * MAX_PATCH).decode()}],
            [{"path": "a", "mode": "100644", "content": "YQ=="}] * 2,
        ]:
            with self.assertRaises(ValueError):
                validate_changes(entries)

    def test_only_fixed_container_execution_and_structured_report_are_exposed(self):
        sandbox = FakeSandbox()
        with tempfile.TemporaryDirectory() as temporary:
            result = Path(temporary) / "result.json"
            tools = mcp_response({"method": "tools/list"}, sandbox, result)["tools"]
            self.assertEqual([t["name"] for t in tools], ["run", "report"])
            with self.assertRaises(ValueError):
                mcp_response({"method": "tools/call", "params": {"name": "host_shell", "arguments": {}}}, sandbox, result)
            answer = report()
            mcp_response({"method": "tools/call", "params": {"name": "report", "arguments": answer}}, sandbox, result)
            self.assertEqual(json.loads(result.read_text()), answer)
            with self.assertRaises(FileExistsError):
                mcp_response({"method": "tools/call", "params": {"name": "report", "arguments": answer}}, sandbox, result)
        with patch.dict(os.environ, {"OPENAI_API_KEY": "provider-secret", "IMPLEMENTATION_APP_PRIVATE_KEY": "app-secret"}):
            settings = config(sandbox, Path("/fixed/result.json"))
        self.assertEqual(settings["permission"], {"*": "deny", "sandbox_*": "allow"})
        self.assertEqual(settings["mcp"]["sandbox"]["command"][:2], ["/usr/bin/env", "-i"])
        self.assertNotIn("provider-secret", json.dumps(settings))
        self.assertNotIn("app-secret", json.dumps(settings))

    def test_discovery_ignores_pr_comments_and_ci_failures_are_deduplicated(self):
        client = FakeGitHub()
        self.assertEqual(discover(client, {"issue": {"number": 8, "pull_request": {}}}, 0), [])
        self.assertEqual(discover(client, {"issue": {"number": 7}}, 0), [7])
        event = {"repository": {"default_branch": "main"}, "workflow_run": {
            "head_branch": "main", "conclusion": "failure", "html_url": "https://github.com/owner/repo/actions/runs/1",
            "head_sha": "a" * 40}}
        existing = []
        writes = []

        def api(method, path, data):
            writes.append((method, path, data))
            if method == "POST":
                existing.append({"number": 11, "body": data["body"]})

        with patch.object(client, "pages", return_value=existing), patch.object(client, "api", side_effect=api):
            track_ci_failure(client, event)
            track_ci_failure(client, event)
        self.assertEqual([w[0] for w in writes], ["POST", "PATCH"])


if __name__ == "__main__":
    unittest.main()
