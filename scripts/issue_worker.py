"""Trusted GitHub issue orchestration. Never execute repository code on this host."""

import argparse
import base64
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
    matches = [c for c in comments if c["user"]["login"] == bot and c["body"].startswith(MARKER)]
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
    return state, comment["id"]


class Worker:
    def __init__(self, client, bot, number, runtime="docker"):
        self.client, self.bot, self.number, self.runtime = client, bot, number, runtime
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
        self.state.update(status=status, message=message[:16000], run=self.run_url)
        body = MARKER + json.dumps(self.state, sort_keys=True) + "\n-->\n" + message[:16000]
        body += f"\n\nState: **{status}** · [worker run]({self.run_url})"
        if len(body) > 60000:
            raise RuntimeError("Durable issue state exceeded size limit")
        if self.comment_id:
            self.client.api("PATCH", f"/issues/comments/{self.comment_id}", {"body": body})
        else:
            self.comment_id = self.client.api("POST", self.path + "/comments", {"body": body})["id"]
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

    def context(self):
        words = set(re.findall(r"\w+", self.issue["title"].lower()))
        issues = [i for i in self.client.pages("/issues?state=all&sort=updated&direction=desc")
                  if i["number"] != self.number and "pull_request" not in i]
        issues.sort(key=lambda i: len(words & set(re.findall(r"\w+", i["title"].lower()))), reverse=True)
        return {
            "issue": {"number": self.number, "title": self.issue["title"], "body": self.issue.get("body")},
            "comments": [{"author": c["user"]["login"], "body": c["body"][:4000]}
                         for c in self.comments if c["user"]["type"] != "Bot"][-10:],
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
                return True
        return False

    def check_pr(self, number):
        pr = self.client.api("GET", f"/pulls/{number}")
        if pr.get("merged"):
            self.save("done", f"Merged {pr['html_url']}; outcome recorded for this issue.")
        elif pr["state"] == "closed":
            self.save("blocked", f"{pr['html_url']} was closed without merging. Resolve its disposition before retrying.")
        else:
            sha = pr["head"]["sha"]
            checks = self.client.api("GET", f"/commits/{sha}/check-runs?filter=latest&per_page=100")["check_runs"]
            statuses = self.client.api("GET", f"/commits/{sha}/status")["statuses"]
            failed = [c["name"] for c in checks if c.get("conclusion") in FAILURES]
            failed += [s["context"] for s in statuses if s["state"] in ("failure", "error")]
            message = f"PR: {pr['html_url']}\n\n"
            message += ("Failing current-head checks: " + ", ".join(sorted(set(failed))) if failed
                        else "Waiting for required CI, independent automated review, and the owner's manual merge.")
            fingerprint = [sha, sorted(set(failed)), pr["state"]]
            if self.state.get("pr_status") != fingerprint:
                self.state["pr_status"] = fingerprint
                self.save("blocked" if failed else "in-progress", message)

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
        tree = []
        for change in changes:
            sha = None
            if change["content"] is not None:
                sha = self.client.api("POST", "/git/blobs", {"encoding": "base64", "content": change["content"]})["sha"]
            tree.append({"path": change["path"], "mode": change["mode"], "type": "blob", "sha": sha})
        tree_sha = self.client.api("POST", "/git/trees", {"base_tree": commit["tree"]["sha"], "tree": tree})["sha"]
        sha = self.client.api("POST", "/git/commits", {"message": f"fix: address issue #{self.number}",
                                                      "tree": tree_sha, "parents": [base]})["sha"]
        self.state.update(commit=sha, branch=f"automation/issue-{self.number}-{self.rev[:12]}",
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
                context["triage"] = triage
                plan = phase(sandbox, "plan", context, self.deadline)
                if plan["status"] != "ready":
                    self.save("needs-information" if plan["status"] == "needs-information" else "blocked", plan["summary"])
                    return
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
                    code, output, _ = sandbox.run(plan["regression"])
                    if not 1 <= code <= 125:
                        raise RuntimeError("Regression check did not fail normally before implementation")
                    evidence += f"\nRegression command: `{plan['regression']}`\n\nBefore fix (exit {code}):\n```text\n{output[-6000:]}\n```\n"
                else:
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
                context["plan"] = plan
                result = phase(sandbox, "implement", context, self.deadline)
                if result["status"] not in ("ready", "complete"):
                    self.save("needs-information" if result["status"] == "needs-information" else "blocked", result["summary"])
                    return
                if plan["kind"] == "bug":
                    self.check(sandbox, plan["regression"])
                self.verify(sandbox)
                context["verification"] = "Regression (if bug), python3 scripts/check.py, and python3 scripts/package_check.py passed."
                result = phase(sandbox, "complete", context, self.deadline)
                if result["status"] != "complete":
                    self.save("needs-information" if result["status"] == "needs-information" else "blocked", result["summary"])
                    return
                # Completion can update artifacts. Verify the exact resulting tree again.
                if plan["kind"] == "bug":
                    self.check(sandbox, plan["regression"])
                self.verify(sandbox)
                # Re-fetch task data; do not publish a result for a superseded revision.
                current = self.client.api("GET", self.path)
                comments = list(self.client.pages(self.path + "/comments"))
                if current["state"] != "open" or revision(current, comments) != self.rev:
                    self.save("blocked", "Issue changed or closed during implementation; result was not published. Reapply ready after triage.")
                    return
                self.publish(sandbox.changes(), result, evidence + "\n" + context["verification"])
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
    required = ("IMPLEMENTATION_APP_ID", "IMPLEMENTATION_APP_PRIVATE_KEY", "OPENAI_API_KEY")
    missing = [name for name in required if not os.environ.get(name)]
    if missing:
        print(json.dumps({"active": False, "missing": missing}))
        raise SystemExit(1)
    client, bot = app_client()
    try:
        ensure_labels(client)
        if args.issue:
            Worker(client, bot, args.issue, args.runtime).execute()
        else:
            track_ci_failure(client, event)
    finally:
        client.request("DELETE", "/installation/token")


if __name__ == "__main__":
    main()
