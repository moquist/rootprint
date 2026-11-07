"""Trusted GitHub issue orchestration. Never execute repository code on this host."""

import argparse
import base64
import copy
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import subprocess
import tempfile
import time
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.request import Request, urlopen

from worker_agent import phase
from worker_sandbox import ROOT, Sandbox, safe_path, validate_changes
from worker_repair import checks as repair_checks, fingerprint as repair_fingerprint, overlay

STATES = ("triage", "needs-information", "ready", "in-progress", "blocked", "done")
MARKER = "<!-- rootprint-worker-state\n"
FAILURE_MARKER = "<!-- rootprint-default-ci-failure -->"
FAILURES = {"failure", "timed_out", "action_required", "startup_failure"}


class ApiError(RuntimeError):
    def __init__(self, status):
        super().__init__(f"GitHub API request failed (HTTP {status})")
        self.status = status


class GitHub:
    def __init__(self, token, repo):
        if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repo):
            raise ValueError("Invalid repository identifier")
        self.token, self.repo = token, repo

    def request(self, method, path, data=None):
        if not path.startswith("/") or path.startswith("//"):
            raise ValueError("Expected a GitHub API path")
        request = Request("https://api.github.com" + path, method=method,
                          data=None if data is None else json.dumps(data).encode(),
                          headers={"Authorization": "Bearer " + self.token,
                                   "Accept": "application/vnd.github+json", "Content-Type": "application/json",
                                   "X-GitHub-Api-Version": "2022-11-28", "User-Agent": "rootprint-worker"})
        try:
            with urlopen(request, timeout=30) as response:
                body = response.read(8 * 1024 * 1024 + 1)
        except HTTPError as error:
            raise ApiError(error.code) from None
        if len(body) > 8 * 1024 * 1024:
            raise ValueError("GitHub response exceeded limit")
        return json.loads(body) if body else None

    def api(self, method, path, data=None):
        return self.request(method, f"/repos/{self.repo}{path}", data)

    def pages(self, path):
        for page in range(1, 101):
            values = self.api("GET", path + ("&" if "?" in path else "?") + f"per_page=100&page={page}")
            yield from values
            if len(values) < 100:
                return
        raise RuntimeError("GitHub pagination limit reached")


APP_PERMISSIONS = {
    "IMPLEMENTATION": {"contents": "write", "issues": "write", "pull_requests": "write"},
    "REVIEWER": {"contents": "read", "pull_requests": "read", "checks": "write"},
}


def app_client(role="IMPLEMENTATION"):
    permissions = APP_PERMISSIONS[role]

    def b64(data):
        return base64.urlsafe_b64encode(data).rstrip(b"=")

    now = int(time.time())
    jwt = b64(b'{"alg":"RS256","typ":"JWT"}') + b"." + b64(json.dumps(
        {"iat": now - 60, "exp": now + 540, "iss": os.environ[f"{role}_APP_ID"]}).encode())
    # NamedTemporaryFile is private (0600); it is never mounted into the sandbox.
    with tempfile.NamedTemporaryFile() as key:
        key.write(os.environ[f"{role}_APP_PRIVATE_KEY"].encode())
        key.flush()
        signature = subprocess.run(["openssl", "dgst", "-sha256", "-sign", key.name], input=jwt,
                                   capture_output=True, check=True).stdout
    client = GitHub((jwt + b"." + b64(signature)).decode(), os.environ["GITHUB_REPOSITORY"])
    app = client.request("GET", "/app")
    installation = client.api("GET", "/installation")
    token = client.request("POST", f"/app/installations/{installation['id']}/access_tokens", {
        "repositories": [client.repo.split("/")[1]],
        "permissions": permissions,
    })
    return GitHub(token["token"], client.repo), app["slug"] + "[bot]"


def revision(issue, comments):
    # Reopening, labels, bot comments, and replayed events do not reset the budget.
    information = [(c["id"], c["body"]) for c in comments if c["user"]["type"] != "Bot"
                   and c["body"].strip() != "/rootprint retry"]
    data = [issue["title"], issue.get("body") or "", information]
    return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()


def load_state(comments, bot):
    matches = [c for c in comments if c["user"]["login"] == bot and c["user"]["type"] == "Bot"
               and c["body"].startswith(MARKER)]
    if len(matches) > 1:
        raise RuntimeError("Multiple worker state records; reconciliation needs investigation")
    if not matches:
        return {}, None
    comment = matches[0]
    state = json.loads(comment["body"][len(MARKER):].split("\n-->", 1)[0])
    if (not isinstance(state, dict) or state.get("status") not in STATES
            or not isinstance(state.get("attempts"), dict)
            or any(not re.fullmatch(r"[a-f0-9]{64}", r) or type(n) is not int or not 0 <= n <= 3
                   for r, n in state["attempts"].items())):
        raise ValueError("Invalid durable worker state")
    if "clarifications" not in state and state["status"] == "needs-information" and state.get("message"):
        # Legacy state did not record the original revision/cursor; do not guess them.
        state["clarifications"] = [{"question": state["message"], "revision": None,
                                    "run": state.get("run"), "after_comment": None}]
    validate_clarifications(state.get("clarifications", []))
    return state, comment["id"]


def validate_clarifications(history):
    if not isinstance(history, list):
        raise ValueError("Invalid durable clarification history")
    seen = set()
    for entry in history:
        if (not isinstance(entry, dict) or set(entry) != {"question", "revision", "run", "after_comment"}
                or not isinstance(entry["question"], str) or not entry["question"].strip()
                or (entry["revision"] is not None and (not isinstance(entry["revision"], str)
                    or not re.fullmatch(r"[a-f0-9]{64}", entry["revision"])))
                or (entry["run"] is not None and (not isinstance(entry["run"], str)
                    or not re.fullmatch(r"https://[^\s]+/actions/runs/(?:[0-9]+|local)", entry["run"])))
                or (entry["after_comment"] is not None
                    and (type(entry["after_comment"]) is not int or entry["after_comment"] < 0))):
            raise ValueError("Invalid durable clarification history")
        key = (entry["revision"], entry["question"])
        if key in seen:
            raise ValueError("Duplicate durable clarification history")
        seen.add(key)


class Worker:
    def __init__(self, client, bot, number, runtime="docker", reader=None, reviewer_app=None):
        self.client, self.bot, self.number, self.runtime = client, bot, number, runtime
        self.reader = reader or client
        self.reviewer_app = int(reviewer_app if reviewer_app is not None else os.environ.get("REVIEWER_APP_ID", "0"))
        self.path = f"/issues/{number}"
        self.issue = client.api("GET", self.path)
        self.comments = list(client.pages(self.path + "/comments"))
        self.state, self.comment_id = load_state(self.comments, bot)
        self.rev = revision(self.issue, self.comments)
        self.state.setdefault("attempts", {})
        self.run_url = os.environ.get("GITHUB_SERVER_URL", "https://github.com") + "/" + client.repo + "/actions/runs/" + os.environ.get("GITHUB_RUN_ID", "local")
        self.deadline = time.monotonic() + 22 * 60

    def save(self, status, message):
        if status not in STATES:
            raise ValueError("Unknown issue state")
        candidate = dict(self.state)
        if "clarifications" in candidate:
            candidate["clarifications"] = copy.deepcopy(candidate["clarifications"])
        if status == "needs-information":
            history = candidate.setdefault("clarifications", [])
            if not any(c["revision"] == self.rev and c["question"] == message for c in history):
                history.append({"question": message, "revision": self.rev, "run": self.run_url,
                                "after_comment": max((c["id"] for c in self.comments
                                                      if c["user"]["type"] != "Bot"), default=0)})
        validate_clarifications(candidate.get("clarifications", []))
        candidate.update(status=status, message=message[:16000], run=self.run_url)
        body = MARKER + json.dumps(candidate, sort_keys=True) + "\n-->\n" + message[:16000]
        body += f"\n\nState: **{status}** · [worker run]({self.run_url})"
        if len(body) > 60000:
            raise RuntimeError("Durable issue state exceeded size limit")
        if self.comment_id:
            self.client.api("PATCH", f"/issues/comments/{self.comment_id}", {"body": body})
        else:
            self.comment_id = self.client.api("POST", self.path + "/comments", {"body": body})["id"]
        self.state = candidate
        # Only touch lifecycle labels, preserving labels applied by the owner.
        for label in STATES:
            if label == status:
                self.client.api("POST", self.path + "/labels", {"labels": [label]})
            else:
                try:
                    self.client.api("DELETE", self.path + "/labels/" + label)
                except ApiError as error:
                    if error.status != 404:
                        raise

    def clarification_context(self):
        validate_clarifications(self.state.get("clarifications", []))
        return {
            "comments": [{"id": c["id"], "author": c["user"]["login"], "body": c["body"]}
                         for c in self.comments if c["user"]["type"] != "Bot"],
            "clarifications": {"author": self.bot, "state_comment": self.comment_id,
                               "history": copy.deepcopy(self.state.get("clarifications", []))},
        }

    def context(self):
        words = set(re.findall(r"\w+", self.issue["title"].lower()))
        issues = [i for i in self.client.pages("/issues?state=all&sort=updated&direction=desc")
                  if i["number"] != self.number and "pull_request" not in i]
        issues.sort(key=lambda i: len(words & set(re.findall(r"\w+", i["title"].lower()))), reverse=True)
        return {
            "issue": {"number": self.number, "title": self.issue["title"], "body": self.issue.get("body")},
            **self.clarification_context(),
            "possibleDuplicates": [{"number": i["number"], "title": i["title"], "body": (i.get("body") or "")[:1000]}
                                   for i in issues[:10]],
        }

    def retry_request(self):
        seen = self.state.get("retry_comment", 0)
        for comment in self.comments:
            if comment["id"] <= seen or comment["body"].strip() != "/rootprint retry":
                continue
            login = quote(comment["user"]["login"], safe="")
            try:
                permission = self.client.api("GET", f"/collaborators/{login}/permission")["permission"]
            except ApiError as error:
                if error.status == 404:
                    continue
                raise
            if permission in ("admin", "maintain", "write"):
                self.state["attempts"][self.rev] = 0
                self.state.pop("triage_revision", None)
                self.state.pop("triage_errors", None)
                self.state["retry_comment"] = comment["id"]
                if not self.state.get("repair", {}).get("pending"):
                    self.state.pop("repair", None)
                return True
        return False

    def authorize_repair(self, pr):
        """Never adopt a different PR/branch, even in response to an owner retry."""
        if (self.issue["state"] != "open" or pr.get("draft") or pr["state"] != "open"
                or pr.get("user", {}).get("login") != self.bot
                or pr["head"].get("repo", {}).get("full_name") != self.client.repo
                or pr["head"].get("ref") != self.state.get("branch")
                or pr["base"].get("repo", {}).get("full_name") != self.client.repo
                or pr["base"]["ref"] != self.state.get("default_branch")):
            self.save("blocked", "Repair paused: issue/PR is closed, draft, foreign, or differs from the authorized worker branch.")
            return False
        retry = self.retry_request()
        ready = "ready" in {label["name"] for label in self.issue["labels"]}
        if self.state.get("repair_revision") != self.rev or retry:
            if not (ready or retry):
                self.save("blocked", "Repair needs authorization for this issue revision. Apply `ready` or an eligible `/rootprint retry`.")
                return False
            self.state["repair_revision"] = self.rev
            self.save("in-progress", "Authorized bounded repairs on the existing worker PR; owner still merges manually.")
        return True

    def reserve_repair(self, key, pr):
        previous = self.state.get("repair", {})
        if previous.get("key") == key and previous.get("stage") in ("finished", "blocked", "needs-information"):
            return False
        attempts = self.state["attempts"].get(self.rev, 0)
        if attempts >= 3:
            self.save("blocked", "Three attempts exhausted for this issue revision. Supply new information and ready, or an eligible `/rootprint retry`.")
            return False
        self.state["attempts"][self.rev] = attempts + 1
        self.state["repair"] = {"key": key, "head": pr["head"]["sha"], "base": pr["base"]["sha"],
                                "revision": self.rev, "attempt": attempts + 1, "stage": "reserved", "run": self.run_url}
        self.state.setdefault("runs", []).append({"revision": self.rev, "attempt": attempts + 1, "url": self.run_url})
        self.save("in-progress", f"Repairing PR #{pr['number']}, head `{pr['head']['sha']}`; attempt {attempts + 1}/3.")
        return True

    def check_pr(self, number):
        pr = self.client.api("GET", f"/pulls/{number}")
        if pr.get("merged"):
            self.save("done", f"Merged {pr['html_url']}; outcome recorded for this issue.")
        elif pr["state"] == "closed":
            self.save("blocked", f"{pr['html_url']} was closed without merging. Resolve its disposition before retrying.")
        else:
            if not self.authorize_repair(pr):
                return
            try:
                if self.state.get("repair", {}).get("pending"):
                    self.recover_repair(pr)
                    return
                evidence = repair_checks(self.reader, pr, self.reviewer_app)
                key = repair_fingerprint(evidence)
                if evidence["stage"] == "repair":
                    self.repair_pr(pr, evidence, key)
                elif self.state.get("pr_status") != [evidence["head"], evidence["base"], evidence["stage"], evidence.get("task")]:
                    # An identical ready/waiting stage must not rewrite the ledger
                    # for every newly-issued review check and cause a review loop.
                    self.state["pr_status"] = [evidence["head"], evidence["base"], evidence["stage"], evidence.get("task")]
                    message = ("Ready for owner's manual rebase merge; current-head CI and independent review passed."
                               if evidence["stage"] == "ready" else "Waiting for fresh required CI and independent review.")
                    self.save("in-progress", f"PR: {pr['html_url']}\n\n{message}")
            except Exception as error:
                # A state-save response can be lost too. Recover the durable record
                # before recording failure, rather than erasing a pending publication.
                self.state, self.comment_id = load_state(list(self.client.pages(self.path + "/comments")), self.bot)
                repair = self.state.get("repair", {})
                if not repair.get("pending"):
                    repair["stage"] = "blocked"
                detail = str(error)[:500] if type(error) in (ValueError, RuntimeError, ApiError, TimeoutError) else type(error).__name__
                message = f"Repair blocked ({type(error).__name__}): {detail}. No merge requested; inspect this run or use an eligible retry."
                if self.state.get("message") != message:
                    self.save("blocked", message)

    def develop(self, sandbox, context, triage):
        """The same plan/implement/complete verification path for initial work and repairs."""
        context["triage"] = triage
        plan = phase(sandbox, "plan", context, self.deadline)
        if plan["status"] != "ready":
            self.pause_phase(plan)
            return None
        contract = safe_path(plan["contract"])
        if plan["kind"] != triage["kind"]:
            raise ValueError("Plan changed issue classification; clarify requirements before implementation")
        if not contract.startswith("openspec/"):
            raise ValueError("Plan must reference an OpenSpec contract")
        self.check(sandbox, "test -f " + shlex.quote(contract))
        evidence = f"Contract/plan: `{contract}`.\n"
        if plan["kind"] == "bug":
            if not plan["regression"].strip():
                raise ValueError("Bug plan omitted runnable regression evidence")
            code, output, truncated = sandbox.run(plan["regression"])
            if not 1 <= code <= 125 or truncated:
                raise RuntimeError("Regression check did not fail normally before implementation or its evidence was truncated")
            evidence += f"\nRegression command: `{plan['regression']}`\n\nBefore fix (exit {code}):\n```text\n{output[-6000:]}\n```\n"
        elif plan["kind"] == "feature":
            planned = sandbox.changes()
            if not any(c["path"].startswith("openspec/changes/") and c["content"] for c in planned):
                raise ValueError("Feature plan did not produce OpenSpec artifacts")
            if not re.fullmatch(r"openspec/changes/[a-z0-9-]+/tasks\.md", contract):
                raise ValueError("Feature contract must identify its change's tasks.md")
            folder = contract.removesuffix("/tasks.md")
            self.check(sandbox, " && ".join("test -f " + shlex.quote(folder + "/" + name)
                                           for name in ("proposal.md", "design.md", "tasks.md"))
                       + " && test -d " + shlex.quote(folder + "/specs")
                       + " && node_modules/.bin/openspec validate " + shlex.quote(folder.split("/")[-1]) + " --strict")
        elif plan["kind"] != "maintenance" or "repair" not in context:
            raise ValueError("Maintenance classification is restricted to non-code repair acceptance")
        elif not plan["regression"].strip():
            raise ValueError("Non-code repair plan omitted its runnable acceptance check")
        context["plan"] = plan
        for name in ("implement", "complete"):
            result = phase(sandbox, name, context, self.deadline)
            if result["status"] not in (("ready", "complete") if name == "implement" else ("complete",)):
                self.pause_phase(result)
                return None
            if plan["kind"] in ("bug", "maintenance"):
                self.check(sandbox, plan["regression"])
            self.verify(sandbox)
            context["verification"] = "Regression/acceptance (if applicable), python3 scripts/check.py, and python3 scripts/package_check.py passed."
        return result, evidence + "\n" + context["verification"]

    def pause_phase(self, result):
        status = "needs-information" if result["status"] == "needs-information" else "blocked"
        if self.state.get("repair"):
            self.state["repair"]["stage"] = status
        self.save(status, result["summary"])

    def repair_pr(self, pr, evidence, key):
        if not self.reserve_repair(key, pr):
            return
        from independent_review import metadata

        context = {"issue": {"number": self.number, "title": self.issue["title"], "body": self.issue.get("body")},
                   **self.clarification_context(),
                   "repair": evidence, "discussion": metadata(self.reader, self.reader, pr["number"])}
        repair_fingerprint(context)  # Check the COMPLETE task, not just individual diagnostics.
        seed = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
        changes = overlay(self.reader, seed, pr["head"]["sha"])
        with Sandbox(self.runtime) as sandbox:
            sandbox.import_head(changes)
            triage = phase(sandbox, "triage", context, self.deadline)
            if triage["status"] != "ready" or triage["duplicates"]:
                self.pause_phase(triage)
                return
            self.check(sandbox, "git reset --hard " + sandbox.base + " && git clean -fd")
            developed = self.develop(sandbox, context, triage)
            if developed is None:
                return
            result, verification = developed
            exported = sandbox.changes()
            if context["plan"]["kind"] == "maintenance" and any(
                    not (c["path"].endswith((".md", ".txt", ".rst")) or c["path"].endswith("/.openspec.yaml"))
                    for c in exported):
                raise ValueError("Non-code maintenance repair changed executable/configuration source; classify code work as bug or feature")
            self.assert_repair_current(pr, key)
            commit = self.client.api("GET", "/git/commits/" + pr["head"]["sha"])
            tree = self.make_tree(exported, commit["tree"]["sha"])
            now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            identity = {"name": "Rootprint worker", "email": "worker@invalid", "date": now}
            self.state["repair"]["pending"] = {
                "message": f"fix: repair PR #{pr['number']} for issue #{self.number}",
                "tree": tree, "parents": [pr["head"]["sha"]], "author": identity, "committer": identity}
            self.state["repair"]["summary"] = (result["summary"] + "\n\n" + verification)[:16000]
            self.save("in-progress", "Repair verified; recovering/publishing a non-force child commit on the existing PR.")
            self.recover_repair(pr)

    def make_tree(self, changes, base_tree):
        tree = []
        for change in validate_changes(changes):
            oid = None
            if change["content"] is not None:
                oid = self.client.api("POST", "/git/blobs", {"encoding": "base64", "content": change["content"]})["sha"]
            tree.append({"path": change["path"], "mode": change["mode"], "type": "blob", "sha": oid})
        return self.client.api("POST", "/git/trees", {"base_tree": base_tree, "tree": tree})["sha"]

    def assert_repair_current(self, expected, key):
        current = self.client.api("GET", f"/pulls/{expected['number']}")
        issue = self.client.api("GET", self.path)
        comments = list(self.client.pages(self.path + "/comments"))
        def identity(p):
            return [p["number"], p["state"], p.get("draft"), p["user"]["login"],
                    p["head"]["sha"], p["head"]["ref"], p["head"]["repo"]["full_name"],
                    p["base"]["sha"], p["base"]["ref"], p["base"]["repo"]["full_name"]]
        if (issue["state"] != "open" or revision(issue, comments) != self.state["repair"]["revision"]
                or identity(current) != identity(expected)
                or repair_fingerprint(repair_checks(self.reader, current, self.reviewer_app)) != key):
            raise ValueError("Issue, PR head/base/identity or applicable failure changed during repair; stale result not published")

    def recover_repair(self, pr):
        repair = self.state["repair"]
        intent = repair["pending"]
        if "candidate" not in repair:
            repair["candidate"] = self.client.api("POST", "/git/commits", intent)["sha"]
            self.save("in-progress", "Repair commit recorded; checking the branch before non-force publication.")
        candidate = repair["candidate"]
        head = pr["head"]["sha"]
        if head != candidate:
            comparison = self.client.api("GET", f"/compare/{candidate}...{head}?per_page=1")
            if comparison.get("status") not in ("ahead", "identical"):
                if head != repair["head"]:
                    raise ValueError("Worker branch changed; pending repair cannot overwrite intervening commits")
                self.assert_repair_current(pr, repair["key"])
                self.client.api("PATCH", "/git/refs/heads/" + quote(self.state["branch"], safe="/"),
                                {"sha": candidate, "force": False})
        self.state["commit"] = candidate
        repair["stage"] = "finished"
        del repair["pending"]
        self.state.pop("pr_status", None)
        self.save("in-progress", f"Published repair `{candidate}` on PR #{pr['number']}. Waiting for fresh CI/review and owner manual merge.\n\n"
                  + repair.get("summary", ""))

    def open_pr(self):
        branch = self.state["branch"]
        existing = self.client.api("GET", "/pulls?state=all&head=" + quote(self.client.repo.split("/")[0] + ":" + branch, safe=""))
        if existing:
            pr = existing[0]
            if (pr["head"]["sha"] != self.state["commit"] or pr["head"]["repo"]["full_name"] != self.client.repo
                    or pr["base"]["ref"] != self.state["default_branch"]):
                raise RuntimeError("Existing PR differs from the pending publication; refusing to adopt it")
        else:
            try:
                self.client.api("POST", "/git/refs", {"ref": "refs/heads/" + branch, "sha": self.state["commit"]})
            except ApiError as error:
                if error.status != 422:
                    raise
                ref = self.client.api("GET", "/git/ref/heads/" + branch)
                if ref["object"]["sha"] != self.state["commit"]:
                    raise RuntimeError("Existing worker branch differs; refusing to overwrite it") from None
            pr = self.client.api("POST", "/pulls", {
                "title": f"Fix #{self.number}: {self.issue['title']}"[:240], "head": branch,
                "base": self.state["default_branch"],
                "body": self.state["pr_body"] + f"\n\nCloses #{self.number}.\n\n[Worker evidence]({self.run_url}).\n"
                        "Requires current-head CI and independent automated review. Owner merges manually.",
            })
        self.state["pr"] = pr["number"]
        self.save("in-progress", f"Prepared {pr['html_url']}. Waiting for required checks and the owner's manual merge.")

    def publish(self, changes, report, evidence):
        changes = validate_changes(changes)
        base = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
        commit = self.client.api("GET", "/git/commits/" + base)
        tree_sha = self.make_tree(changes, commit["tree"]["sha"])
        sha = self.client.api("POST", "/git/commits", {"message": f"fix: address issue #{self.number}",
                                                      "tree": tree_sha, "parents": [base]})["sha"]
        self.state.update(commit=sha, branch=f"automation/issue-{self.number}-{self.rev[:12]}",
                          repair_revision=self.rev,
                          default_branch=self.client.api("GET", "")["default_branch"],
                          pr_body=report["summary"] + "\n\n" + evidence)
        # Persist before branch/PR writes, so a lost response can be reconciled.
        self.save("in-progress", "Verification passed; publishing the implementation branch and linked PR.")
        self.open_pr()

    def execute(self):
        if "pull_request" in self.issue:
            return
        if self.state.get("pr"):
            self.check_pr(self.state["pr"])
            return
        if self.state.get("commit"):
            self.open_pr()
            return
        if self.issue["state"] != "open" or "automation-failure" in {label["name"] for label in self.issue["labels"]}:
            return
        retry = self.retry_request()
        ready = ("ready" in {label["name"] for label in self.issue["labels"]} or retry
                 or self.state.get("status") == "in-progress")
        attempts = self.state["attempts"].get(self.rev, 0)
        if attempts >= 3:
            if self.state.get("status") != "blocked":
                self.save("blocked", "Three attempts exhausted for this issue revision. Supply new information or an authorized `/rootprint retry`.")
            return
        if self.state.get("triage_revision") == self.rev and not ready:
            return
        errors = self.state.get("triage_errors", {})
        if errors.get(self.rev, 0) >= 3:
            return
        if ready:
            self.state["attempts"][self.rev] = attempts + 1
            self.state.setdefault("runs", []).append({"revision": self.rev, "attempt": attempts + 1, "url": self.run_url})
            self.save("in-progress", f"Starting attempt {attempts + 1}/3 for revision `{self.rev[:12]}`.")
        else:
            errors[self.rev] = errors.get(self.rev, 0) + 1
            self.state["triage_errors"] = errors
            self.save("triage", "Inspecting the report; implementation still requires the owner's ready label.")
        try:
            context = self.context()
            if len(json.dumps(context)) > 90000:
                raise ValueError("Issue context exceeds the worker input limit")
            with Sandbox(self.runtime) as sandbox:
                triage = phase(sandbox, "triage", context, self.deadline)
                self.state["triage_revision"] = self.rev
                duplicates = "\n\nLikely duplicates: " + ", ".join(f"#{n}" for n in triage["duplicates"]) if triage["duplicates"] else ""
                if triage["status"] != "ready" or triage["duplicates"]:
                    status = "needs-information" if triage["status"] == "needs-information" else "blocked"
                    self.save(status, triage["summary"] + duplicates)
                    return
                if not ready:
                    self.save("triage", triage["summary"] + "\n\nOwner: apply `ready` to authorize an implementation attempt.")
                    return
                self.check(sandbox, "git reset --hard " + sandbox.base + " && git clean -fd")
                developed = self.develop(sandbox, context, triage)
                if developed is None:
                    return
                result, evidence = developed
                # Re-fetch task data; do not publish a result for a superseded revision.
                current = self.client.api("GET", self.path)
                comments = list(self.client.pages(self.path + "/comments"))
                if current["state"] != "open" or revision(current, comments) != self.rev:
                    self.save("blocked", "Issue changed or closed during implementation; result was not published. Reapply ready after triage.")
                    return
                self.publish(sandbox.changes(), result, evidence)
        except Exception as error:
            # Never copy provider/process exception bodies, environment, or secret-bearing logs into GitHub.
            kind = type(error).__name__
            detail = str(error)[:500] if type(error) in (RuntimeError, ValueError, TimeoutError, ApiError) else kind
            self.save("blocked", f"Worker attempt stopped ({kind}): {detail}. No merge was requested. "
                      "Inspect the linked run and configuration; supply new information or use `/rootprint retry` if eligible.")
            raise RuntimeError("Worker attempt stopped; diagnostics recorded on its issue") from None

    def check(self, sandbox, script):
        if time.monotonic() > self.deadline - 10:
            raise TimeoutError("Worker deadline exhausted")
        code, _, _ = sandbox.run(script, timeout=min(300, max(1, int(self.deadline - time.monotonic()))))
        if code:
            raise RuntimeError("Sandbox verification command failed")

    def verify(self, sandbox):
        self.check(sandbox, "python3 scripts/check.py && python3 scripts/package_check.py")


def ensure_labels(client):
    existing = {label["name"] for label in client.pages("/labels")}
    for name in (*STATES, "automation-failure"):
        if name not in existing:
            try:
                client.api("POST", "/labels", {"name": name, "color": "5319e7"})
            except ApiError as error:
                if error.status != 422:
                    raise


def track_ci_failure(client, event):
    run = event.get("workflow_run", {})
    default = event.get("repository", {}).get("default_branch")
    if run.get("head_branch") != default or run.get("conclusion") not in FAILURES:
        return
    issues = [i for i in client.pages("/issues?state=open&labels=automation-failure") if "pull_request" not in i]
    body = FAILURE_MARKER + f"\nDefault-branch CI failed: {run['html_url']}\nRevision: `{run['head_sha']}`."
    for issue in issues:
        if (issue.get("body") or "").startswith(FAILURE_MARKER):
            client.api("PATCH", f"/issues/{issue['number']}", {"body": body})
            return
    client.api("POST", "/issues", {"title": "Default-branch CI failure", "body": body,
                                   "labels": ["automation-failure", "blocked"]})


def discover(client, event, number):
    if number:
        return [number]
    if event.get("issue") and "pull_request" not in event["issue"]:
        return [event["issue"]["number"]]
    if "issue" in event:
        return []
    issues = [i["number"] for i in client.pages("/issues?state=all&sort=updated&direction=desc")
              if "pull_request" not in i and (i["state"] == "open" or
                 any(label["name"] in ("in-progress", "blocked") for label in i["labels"]))]
    run = event.get("workflow_run", {})
    if run.get("conclusion") in FAILURES and run.get("head_branch") == event.get("repository", {}).get("default_branch"):
        issues.insert(0, 0)
    if len(issues) > 200:
        raise RuntimeError("More than 200 candidate issues; partition reconciliation before enabling at this scale")
    return issues


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["discover", "run"])
    parser.add_argument("--issue", type=int, default=0)
    parser.add_argument("--runtime", choices=["docker", "podman"], default="docker")
    args = parser.parse_args()
    if args.issue < 0:
        parser.error("Issue number must be nonnegative")
    event = json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_text(encoding="utf-8"))
    if args.mode == "discover":
        numbers = discover(GitHub(os.environ["GITHUB_TOKEN"], os.environ["GITHUB_REPOSITORY"]), event, args.issue)
        print(json.dumps(numbers))
        return
    required = ("IMPLEMENTATION_APP_ID", "IMPLEMENTATION_APP_PRIVATE_KEY", "OPENAI_API_KEY", "GITHUB_TOKEN", "REVIEWER_APP_ID")
    missing = [name for name in required if not os.environ.get(name)]
    if missing:
        print(json.dumps({"active": False, "missing": missing}))
        raise SystemExit(1)
    client, bot = app_client()
    try:
        ensure_labels(client)
        if args.issue:
            Worker(client, bot, args.issue, args.runtime,
                   reader=GitHub(os.environ["GITHUB_TOKEN"], client.repo)).execute()
        else:
            track_ci_failure(client, event)
    finally:
        client.request("DELETE", "/installation/token")


if __name__ == "__main__":
    main()
