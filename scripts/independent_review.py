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
IMAGE_SUFFIXES = (".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".ico", ".bmp", ".tif", ".tiff", ".avif", ".apng")
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


class ProviderError(RuntimeError):
    def __init__(self, status):
        self.status = status
        super().__init__(f"OpenAI review request failed (HTTP {status})")


class ReviewFailure(RuntimeError):
    def __init__(self, detail, summary):
        super().__init__(detail)
        self.summary = summary


def sha(value):
    if not isinstance(value, str) or not re.fullmatch(r"[a-f0-9]{40}", value):
        raise ValueError("Invalid Git object SHA")
    return value


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def compact(value):
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


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
    if len(compact(result).encode()) > MAX_CONTEXT:
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

    def blob_bytes(entry, limit):
        if entry["type"] != "blob" or entry["mode"] not in ("100644", "100755"):
            raise ValueError("Unsupported symlink or submodule in review context")
        if not 0 <= entry.get("size", limit + 1) <= limit:
            raise ValueError("File exceeds review size limit")
        object_id = sha(entry["sha"])
        if object_id not in cache:
            blob = client.api("GET", "/git/blobs/" + object_id)
            if blob["encoding"] != "base64" or blob.get("size", entry["size"]) != entry["size"]:
                raise ValueError("Unsupported Git blob encoding")
            encoded = blob["content"].replace("\n", "").replace("\r", "")
            if len(encoded) > 4 * ((limit + 2) // 3):
                raise ValueError("File exceeds review size limit")
            cache[object_id] = base64.b64decode(encoded, validate=True)
        if len(cache[object_id]) > limit or len(cache[object_id]) != entry["size"]:
            raise ValueError("Git blob size does not match bounded tree entry")
        return cache[object_id]

    def text(entry):
        raw = blob_bytes(entry, MAX_FILE)
        if b"\0" in raw:
            raise ValueError("Unsupported binary in review context")
        return raw.decode("utf-8")

    omitted_images = sorted(path for path in before.keys() | after.keys() if path.lower().endswith(IMAGE_SUFFIXES))
    for path in changed:
        if path in omitted_images:
            for entries in (before, after):
                if path in entries and (entries[path]["type"] != "blob" or entries[path]["mode"] not in ("100644", "100755")):
                    raise ValueError("Unsupported symlink or submodule in review context")

    # Include complete source for callers, not only a possibly truncated API patch.
    head_files, omitted = {}, []
    for path, entry in sorted(after.items()):
        if path in omitted_images:
            continue
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
    baseline = {path: text(before[path]) for path in changed if path in before and path not in omitted_images}
    # Current base contracts may have advanced since the branch's merge-base.
    current_base = tree(client, data["base"]) if data["base"] != merge_base else before
    contracts = {path: text(entry) for path, entry in current_base.items()
                 if path in ("AGENTS.md", "docs/protocol.md", "openspec/config.yaml")
                 or (path.startswith("openspec/") and path.endswith(".md"))}
    checks = client.api("GET", f"/commits/{data['head']}/check-runs?check_name=ci&filter=latest&per_page=100")["check_runs"]
    changes = [{"path": path, "before_mode": before.get(path, {}).get("mode"),
                "after_mode": after.get(path, {}).get("mode")} for path in changed]
    result = {"pr": data, "merge_base": merge_base, "changes": changes,
              "head_files": head_files, "changed_baseline_files": baseline, "omitted_image_paths": omitted_images,
              "current_base_contracts": contracts, "omitted_unchanged_paths": omitted,
              "ci_evidence": [{"name": c["name"], "app": c["app"]["slug"], "head_sha": c["head_sha"],
                               "status": c["status"], "conclusion": c.get("conclusion")} for c in checks]}
    model_content(result)
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


def model_content(task_data):
    content = [{"type": "input_text", "text": compact(task_data)}]
    if len(content[0]["text"].encode()) > MAX_CONTEXT:
        raise ValueError("Complete review context exceeds size limit; no content was silently truncated")
    return content


def ask_model(task_data):
    if not os.environ.get("OPENAI_API_KEY"):
        raise ValueError("Missing configuration: OPENAI_API_KEY")
    content = model_content(task_data)
    payload = {"model": MODEL.removeprefix("openai/"), "store": False, "tools": [], "tool_choice": "none",
               "max_output_tokens": 10000, "instructions": policy(), "input": [{"role": "user", "content": content}],
               "text": {"format": {"type": "json_schema", "name": "independent_review", "strict": True, "schema": SCHEMA}}}
    request = Request("https://api.openai.com/v1/responses", data=compact(payload).encode(), method="POST",
                      headers={"Authorization": "Bearer " + os.environ["OPENAI_API_KEY"], "Content-Type": "application/json"})
    try:
        with urlopen(request, timeout=600) as response:
            body = response.read(1024 * 1024 + 1)
    except HTTPError as error:
        # Status only: provider bodies/reasons/headers can contain sensitive input.
        status = error.code
        error.close()
        raise ProviderError(status) from None
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


def repair_task(data):
    # Updating the implementation ledger must not turn its own repair input stale.
    value = json.loads(json.dumps(data))
    for issue in value["issues"]:
        issue["comments"] = [c for c in issue["comments"] if not (
            c["author"] == value["author"] and c["body"].startswith("<!-- rootprint-worker-state\n"))]
    return digest(value)


def complete(client, check_id, conclusion, summary, outcome=None, title=None):
    text = compact(outcome or {"schema": "rootprint-review-outcome-v1", "kind": "infrastructure"})
    if len(text.encode()) > 60000:
        raise ValueError("Structured review diagnostics exceed check output limit")
    client.api("PATCH", f"/check-runs/{check_id}", {
        "status": "completed", "conclusion": conclusion,
        "output": {"title": title or "Independent review " + ("passed" if conclusion == "success" else "blocked"),
                   "summary": summary, "text": text},
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
        complete(client, check["id"], "success" if result["decision"] == "approve" else "failure", summary,
                 {"schema": "rootprint-review-outcome-v1",
                  "kind": "approval" if result["decision"] == "approve" else "rejection",
                  "head": data["head"], "base": data["base"], "task": repair_task(data),
                  "result": result})
    except Exception as error:
        # Never publish request bodies, environment values, provider responses, or credential-bearing tracebacks.
        detail = str(error)[:500] if type(error) in (ValueError, RuntimeError, ApiError, ProviderError) else type(error).__name__
        next_step = "Investigate the reported prerequisite or review-input problem before requesting another review."
        title = "Independent review blocked: infrastructure/input failure"
        if isinstance(error, ProviderError):
            title = f"Independent review blocked: OpenAI HTTP {error.status}"
            if error.status == 429:
                next_step = ("Check OpenAI project credits/billing and rate limits. HTTP 429 can mean exhausted quota "
                             "or rate limiting; the status alone does not distinguish them. Resolve quota/billing "
                             "or wait for the rate limit to clear before retrying.")
            elif error.status in (401, 403):
                next_step = "Check the configured OpenAI API key, project permissions and model access before retrying."
            elif 500 <= error.status <= 599:
                next_step = "Check OpenAI service status; wait for the provider failure to clear before retrying."
            else:
                next_step = "Check the OpenAI model/request configuration and provider availability before retrying."
        retry_command = f"gh workflow run independent-review.yml --repo {client.repo} -f pr={number} -f retry=true"
        if isinstance(error, ProviderError):
            next_step += f" After resolution, use `{retry_command}` (at most three attempts per exact review context)."
        summary = (f"## {title}\n\n{detail}.\n\nThis is not a code-review rejection; no approval was produced."
                   f"\n\n### Next step\n\n{next_step}\n\n[PR #{number}](https://github.com/{client.repo}/pull/{number})"
                   f" · [Review run]({run_url}).")
        if check is None:
            # Even failures collecting metadata must replace any earlier success
            # on the same head with a blocking check, without leaking raw input.
            key = "rootprint-review-error:" + digest([head, initial["base"]["sha"], initial["title"], initial.get("body"), detail])
            history = sorted(existing_checks(client, head, bot), key=lambda c: c["id"])
            check = history[-1] if history and history[-1].get("external_id") == key else start(key)
        complete(client, check["id"], "failure", summary, title=title)
        raise ReviewFailure(f"Independent review blocked: {detail}. Next step: {next_step}", summary) from None


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
    except ReviewFailure as error:
        # Emit at the CLI boundary so synthetic review failures in tests do not
        # create Actions annotations or overwrite the actual job's summary.
        message = str(error).replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")
        print("::error title=Independent review blocked::" + message if os.environ.get("GITHUB_ACTIONS") == "true" else str(error))
        if os.environ.get("GITHUB_STEP_SUMMARY"):
            try:
                with Path(os.environ["GITHUB_STEP_SUMMARY"]).open("a", encoding="utf-8") as summary:
                    summary.write(error.summary + "\n")
            except OSError:
                print("Could not write the job summary; see the review failure diagnostic above.")
        raise SystemExit(1) from None
    finally:
        client.request("DELETE", "/installation/token")


if __name__ == "__main__":
    main()
