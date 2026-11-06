"""Tool-free, fresh-context review; only trusted default-branch code runs locally."""

import argparse
import base64
import hashlib
from itertools import islice
import json
import os
from pathlib import Path
import re
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from issue_worker import ApiError, GitHub, app_client
from worker_agent import MODEL

ROOT = Path(__file__).resolve().parents[1]
CHECK = "independent-review"
MAX_CONTEXT = 600000
MAX_FILE = 100000
ASSESSMENTS = ("acceptance", "regression", "error_paths", "compatibility", "trust_boundaries")
SCHEMA = {
    "type": "object", "additionalProperties": False,
    "properties": {
        "reviewed_head": {"type": "string"}, "reviewed_base": {"type": "string"},
        "decision": {"type": "string", "enum": ["approve", "request-changes"]},
        "summary": {"type": "string"},
        "assessments": {"type": "object", "additionalProperties": False,
                        "properties": {key: {"type": "string", "enum": ["pass", "fail", "not-applicable"]}
                                       for key in ASSESSMENTS}, "required": list(ASSESSMENTS)},
        "findings": {"type": "array", "items": {
            "type": "object", "additionalProperties": False,
            "properties": {"severity": {"type": "string", "enum": ["blocking", "warning"]},
                           "path": {"type": "string"}, "line": {"type": "integer"}, "message": {"type": "string"}},
            "required": ["severity", "path", "line", "message"]}},
    },
    "required": ["reviewed_head", "reviewed_base", "decision", "summary", "assessments", "findings"],
}


def sha(value):
    if not isinstance(value, str) or not re.fullmatch(r"[a-f0-9]{40}", value):
        raise ValueError("Invalid Git object SHA")
    return value


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def policy():
    return (ROOT / "automation/reviewer-policy.md").read_text(encoding="utf-8")


def metadata(client, reader, number):
    pr = client.api("GET", f"/pulls/{number}")
    if pr["base"]["repo"]["full_name"] != client.repo:
        raise ValueError("PR base repository does not match installation")
    comments = list(islice(reader.pages(f"/issues/{number}/comments"), 101))
    issues = []
    references = sorted(set(int(n) for n in re.findall(
        r"\b(?:close[sd]?|fix(?:e[sd])?|resolve[sd]?)\s+#([1-9][0-9]*)\b", pr.get("body") or "", re.I)))
    if len(references) > 10 or len(comments) > 100:
        raise ValueError("Review discussion exceeds context limits")
    for linked in references:
        issue = reader.api("GET", f"/issues/{linked}")
        discussion = list(islice(reader.pages(f"/issues/{linked}/comments"), 101))
        if len(discussion) > 100:
            raise ValueError("Linked issue discussion exceeds context limits")
        issues.append({"number": linked, "title": issue["title"], "body": issue.get("body"),
                       "comments": [{"author": c["user"]["login"], "body": c["body"]} for c in discussion]})
    result = {
        "number": number, "title": pr["title"], "body": pr.get("body"), "state": pr["state"],
        "draft": pr["draft"], "author": pr["user"]["login"],
        "head": sha(pr["head"]["sha"]), "base": sha(pr["base"]["sha"]), "base_ref": pr["base"]["ref"],
        "comments": [{"author": c["user"]["login"], "body": c["body"]} for c in comments], "issues": issues,
    }
    if len(json.dumps(result).encode()) > MAX_CONTEXT:
        raise ValueError("Review metadata exceeds context limits")
    return result


def fingerprint(data):
    # Changes to trusted review code/policy or material task data invalidate cached results.
    source = os.environ.get("REVIEW_SOURCE_SHA") or digest(
        [Path(__file__).read_text(encoding="utf-8"), (ROOT / "scripts/issue_worker.py").read_text(encoding="utf-8")])
    return "rootprint-review-v1:" + digest([source, policy(), data])


def tree(client, commit):
    response = client.api("GET", f"/git/trees/{sha(commit)}?recursive=1")
    if response.get("truncated") or len(response["tree"]) > 2000:
        raise ValueError("Git tree is incomplete or exceeds review limits")
    return {entry["path"]: entry for entry in response["tree"] if entry["type"] != "tree"}


def context(client, data):
    def credential_path(path):
        name = path.rsplit("/", 1)[-1]
        return name.startswith(".env") or name.endswith((".pem", ".key"))

    comparison = client.api("GET", f"/compare/{data['base']}...{data['head']}?per_page=1")
    merge_base = sha(comparison["merge_base_commit"]["sha"])
    before, after = tree(client, merge_base), tree(client, data["head"])
    changed = sorted(path for path in before.keys() | after.keys() if
                     (before.get(path, {}).get("sha"), before.get(path, {}).get("mode")) !=
                     (after.get(path, {}).get("sha"), after.get(path, {}).get("mode")))
    if not 1 <= len(changed) <= 100:
        raise ValueError("Review requires 1–100 changed files")
    if any(credential_path(path) for path in changed):
        raise ValueError("Credential-file changes cannot be sent to the review model")
    cache = {}

    def text(entry):
        if entry["type"] != "blob" or entry["mode"] not in ("100644", "100755"):
            raise ValueError("Unsupported symlink or submodule in review context")
        if entry.get("size", MAX_FILE + 1) > MAX_FILE:
            raise ValueError("File exceeds review size limit")
        object_id = sha(entry["sha"])
        if object_id not in cache:
            blob = client.api("GET", "/git/blobs/" + object_id)
            if blob["encoding"] != "base64":
                raise ValueError("Unsupported Git blob encoding")
            raw = base64.b64decode(blob["content"].replace("\n", "").replace("\r", ""), validate=True)
            if len(raw) > MAX_FILE:
                raise ValueError("File exceeds review size limit")
            cache[object_id] = raw.decode("utf-8")
        return cache[object_id]

    # Include complete source for callers, not only a possibly truncated API patch.
    head_files, omitted = {}, []
    for path, entry in sorted(after.items()):
        if credential_path(path) or (path.startswith(".opencode/") and path not in changed):
            omitted.append(path)
            continue
        if len(head_files) >= 500:
            raise ValueError("Repository exceeds review file limit")
        try:
            head_files[path] = text(entry)
        except (UnicodeError, ValueError):
            if path in changed:
                raise
            omitted.append(path)
    baseline = {path: text(before[path]) for path in changed if path in before}
    # Current base contracts may have advanced since the branch's merge-base.
    current_base = tree(client, data["base"]) if data["base"] != merge_base else before
    contracts = {path: text(entry) for path, entry in current_base.items()
                 if path in ("AGENTS.md", "docs/protocol.md", "openspec/config.yaml")
                 or (path.startswith("openspec/") and path.endswith(".md"))}
    checks = client.api("GET", f"/commits/{data['head']}/check-runs?check_name=ci&filter=latest&per_page=100")["check_runs"]
    changes = [{"path": path, "before_mode": before.get(path, {}).get("mode"),
                "after_mode": after.get(path, {}).get("mode")} for path in changed]
    result = {"pr": data, "merge_base": merge_base, "changes": changes,
              "head_files": head_files, "changed_baseline_files": baseline,
              "current_base_contracts": contracts, "omitted_unchanged_paths": omitted,
              "ci_evidence": [{"name": c["name"], "app": c["app"]["slug"], "head_sha": c["head_sha"],
                               "status": c["status"], "conclusion": c.get("conclusion")} for c in checks]}
    if len(json.dumps(result).encode()) > MAX_CONTEXT:
        raise ValueError("Complete review context exceeds size limit; no content was silently truncated")
    return result


def validate_result(result, data, files):
    if not isinstance(result, dict) or set(result) != set(SCHEMA["required"]):
        raise ValueError("Incomplete structured review")
    if result["reviewed_head"] != data["head"] or result["reviewed_base"] != data["base"]:
        raise ValueError("Review refers to different Git revisions")
    if (result["decision"] not in ("approve", "request-changes") or not isinstance(result["summary"], str)
            or not 1 <= len(result["summary"].strip()) <= 3000):
        raise ValueError("Invalid review decision or summary")
    assessments = result["assessments"]
    if (not isinstance(assessments, dict) or set(assessments) != set(ASSESSMENTS)
            or any(value not in ("pass", "fail", "not-applicable") for value in assessments.values())):
        raise ValueError("Incomplete review assessments")
    findings = result["findings"]
    if not isinstance(findings, list) or len(findings) > 20:
        raise ValueError("Invalid review findings")
    for finding in findings:
        if (not isinstance(finding, dict) or set(finding) != {"severity", "path", "line", "message"}
                or finding["severity"] not in ("blocking", "warning") or finding["path"] not in ("", *files)
                or type(finding["line"]) is not int or finding["line"] < 0
                or not isinstance(finding["message"], str) or not 1 <= len(finding["message"].strip()) <= 1500):
            raise ValueError("Invalid review finding")
    if result["decision"] == "approve" and ("fail" in assessments.values()
            or assessments["trust_boundaries"] != "pass" or any(f["severity"] == "blocking" for f in findings)):
        raise ValueError("Approval contradicts blocking review findings or assessments")
    return result


def ask_model(task_data):
    if not os.environ.get("OPENAI_API_KEY"):
        raise ValueError("Missing configuration: OPENAI_API_KEY")
    payload = {"model": MODEL.removeprefix("openai/"), "store": False, "tools": [], "tool_choice": "none",
               "max_output_tokens": 10000, "instructions": policy(), "input": json.dumps(task_data),
               "text": {"format": {"type": "json_schema", "name": "independent_review", "strict": True, "schema": SCHEMA}}}
    request = Request("https://api.openai.com/v1/responses", data=json.dumps(payload).encode(), method="POST",
                      headers={"Authorization": "Bearer " + os.environ["OPENAI_API_KEY"], "Content-Type": "application/json"})
    try:
        with urlopen(request, timeout=600) as response:
            body = response.read(1024 * 1024 + 1)
    except HTTPError as error:
        raise RuntimeError(f"OpenAI review request failed (HTTP {error.code})") from None
    if len(body) > 1024 * 1024:
        raise ValueError("Review response exceeds size limit")
    response = json.loads(body)
    if response.get("status") != "completed":
        raise ValueError("OpenAI review is incomplete")
    texts = []
    for item in response.get("output", []):
        if item.get("type") == "reasoning":
            continue
        if item.get("type") != "message" or item.get("role") != "assistant" or item.get("status") != "completed":
            raise ValueError("Unexpected review output or attempted tool use")
        for content in item["content"]:
            if content.get("type") != "output_text":
                raise ValueError("Review refused or returned non-text content")
            texts.append(content["text"])
    if len(texts) != 1:
        raise ValueError("Expected one structured review response")
    return json.loads(texts[0])


def existing_checks(client, head, bot):
    checks = []
    for page in range(1, 11):
        values = client.api("GET", f"/commits/{head}/check-runs?check_name={CHECK}&filter=all&per_page=100&page={page}")["check_runs"]
        checks.extend(c for c in values if c["name"] == CHECK and c["app"]["slug"] + "[bot]" == bot)
        if len(values) < 100:
            return checks
    raise ValueError("Review check history exceeds pagination limit")


def complete(client, check_id, conclusion, summary):
    client.api("PATCH", f"/check-runs/{check_id}", {
        "status": "completed", "conclusion": conclusion,
        "output": {"title": "Independent review " + ("passed" if conclusion == "success" else "blocked"),
                   "summary": summary},
    })


def review(client, reader, bot, number, retry=False):
    initial = client.api("GET", f"/pulls/{number}")
    if initial["state"] != "open":
        return
    head = sha(initial["head"]["sha"])
    run_url = (os.environ.get("GITHUB_SERVER_URL", "https://github.com") + "/" + client.repo
               + "/actions/runs/" + os.environ.get("GITHUB_RUN_ID", "local"))
    check = None

    def start(key):
        return client.api("POST", "/check-runs", {"name": CHECK, "head_sha": head, "external_id": key,
                                                  "status": "in_progress", "details_url": run_url})

    try:
        data = metadata(client, reader, number)
        head = data["head"]
        key = fingerprint(data)
        history = sorted(existing_checks(client, head, bot), key=lambda c: c["id"])
        previous = [c for c in history if c.get("external_id") == key]
        # Only the latest check can be reused: an older cached failure must never
        # leave a newer success for DIFFERENT task data as the active merge gate.
        if history and history[-1].get("external_id") == key:
            latest = history[-1]
            if latest["status"] == "completed" and (latest.get("conclusion") == "success" or not retry):
                return
        if len(previous) >= 3:
            check = history[-1] if history[-1].get("external_id") == key else start(key)
            raise ValueError("Three review attempts exhausted for this exact revision/context. Supply a new revision or material information")
        check = start(key)
        if data["state"] != "open":
            raise ValueError("PR closed while collecting review context")
        if data["draft"]:
            raise ValueError("Draft PR is not ready for independent approval")
        if data["author"] == bot:
            raise ValueError("Reviewer App cannot approve its own PR")
        task_data = context(client, data)
        files = task_data["head_files"].keys() | task_data["changed_baseline_files"].keys()
        result = validate_result(ask_model(task_data), data, files)
        if metadata(client, reader, number) != data:
            raise ValueError("PR head, base, or material task data changed during review; result is stale")
        assessments = "\n".join(f"- {name}: {result['assessments'][name]}" for name in ASSESSMENTS)
        findings = "\n".join(f"- **{f['severity']}** `{f['path']}:{f['line']}`: {f['message']}" for f in result["findings"])
        summary = (f"Reviewed head `{data['head']}` against base `{data['base']}`.\n\n{result['summary']}\n\n"
                   f"{assessments}\n\n{findings}\n\n[Trusted review run]({run_url}). CI remains a separate required gate.")
        complete(client, check["id"], "success" if result["decision"] == "approve" else "failure", summary)
    except Exception as error:
        # Never publish request bodies, environment values, provider responses, or credential-bearing tracebacks.
        detail = str(error)[:500] if type(error) in (ValueError, RuntimeError, ApiError) else type(error).__name__
        if check is None:
            # Even failures collecting metadata must replace any earlier success
            # on the same head with a blocking check, without leaking raw input.
            key = "rootprint-review-error:" + digest([head, initial["base"]["sha"], initial["title"], initial.get("body"), detail])
            history = sorted(existing_checks(client, head, bot), key=lambda c: c["id"])
            check = history[-1] if history and history[-1].get("external_id") == key else start(key)
        complete(client, check["id"], "failure", "Independent review did not approve: " + detail + f".\n\n[Review run]({run_url}).")
        raise RuntimeError("Independent review stopped; blocking check recorded") from None


def discover(client, event, number=0):
    if number:
        return [number]
    if event.get("pull_request"):
        return [event["pull_request"]["number"]]
    numbers = [pr["number"] for pr in client.pages("/pulls?state=open")]
    if len(numbers) > 200:
        raise ValueError("More than 200 open PRs; partition review reconciliation before enabling at this scale")
    return numbers


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["discover", "run"])
    parser.add_argument("--pr", type=int, default=0)
    parser.add_argument("--retry", action="store_true")
    args = parser.parse_args()
    if args.pr < 0 or (args.mode == "run" and not args.pr):
        parser.error("run requires a positive PR number")
    reader = GitHub(os.environ["GITHUB_TOKEN"], os.environ["GITHUB_REPOSITORY"])
    if args.mode == "discover":
        event = json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_text(encoding="utf-8"))
        print(json.dumps(discover(reader, event, args.pr)))
        return
    missing = [name for name in ("REVIEWER_APP_ID", "REVIEWER_APP_PRIVATE_KEY") if not os.environ.get(name)]
    if missing:
        print(json.dumps({"active": False, "missing": missing}))
        raise SystemExit(1)
    if os.environ["REVIEWER_APP_ID"] == os.environ.get("IMPLEMENTATION_APP_ID"):
        raise RuntimeError("Reviewer and implementation Apps must have different IDs")
    client, bot = app_client("REVIEWER")
    try:
        review(client, reader, bot, args.pr, args.retry)
    finally:
        client.request("DELETE", "/installation/token")


if __name__ == "__main__":
    main()
