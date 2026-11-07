"""Bounded immutable PR data for the trusted worker; never execute PR code here."""

import base64
import hashlib
from itertools import islice
import json
import re

from worker_sandbox import MAX_PATCH, validate_changes

CI_APP = 15368
MAX_CONTEXT = 90000


def sha(value):
    if not isinstance(value, str) or not re.fullmatch(r"[a-f0-9]{40}", value):
        raise ValueError("Invalid repair Git SHA")
    return value


def bounded(values, limit=2000):
    result = list(islice(values, limit + 1))
    if len(result) > limit:
        raise ValueError("Repair evidence exceeds pagination limit")
    return result


def fingerprint(value):
    encoded = json.dumps(value, sort_keys=True)
    if len(encoded) > MAX_CONTEXT:
        raise ValueError("Complete repair context exceeds 90,000 characters")
    return hashlib.sha256(encoded.encode()).hexdigest()


def api_items(reader, path, field):
    items = []
    for page in range(1, 21):
        batch = reader.api("GET", path + ("&" if "?" in path else "?") + f"per_page=100&page={page}")[field]
        items.extend(batch)
        if len(batch) < 100:
            return items
    raise ValueError("Repair diagnostics exceed pagination limit")


def checks(reader, pr, reviewer_app):
    """Return waiting, ready, or complete actionable failure evidence. Fail closed."""
    # Import lazily: the reviewer shares the trusted GitHub client with issue_worker.
    from independent_review import metadata, repair_task, validate_result

    head, base = sha(pr["head"]["sha"]), sha(pr["base"]["sha"])
    values = []
    for page in range(1, 21):
        response = reader.api("GET", f"/commits/{head}/check-runs?filter=latest&per_page=100&page={page}")
        batch = response["check_runs"]
        values.extend(batch)
        if len(batch) < 100:
            break
    else:
        raise ValueError("Repair check history exceeds pagination limit")
    gates = {}
    for name, app in (("ci", CI_APP), ("independent-review", reviewer_app)):
        matches = [c for c in values if c["name"] == name and c.get("head_sha") == head
                   and c.get("app", {}).get("id") == app]
        if not matches:
            return {"stage": "waiting", "head": head, "base": base}
        gates[name] = max(matches, key=lambda c: c["id"])
    if any(c["status"] != "completed" for c in gates.values()):
        return {"stage": "waiting", "head": head, "base": base}
    task = metadata(reader, reader, pr["number"])
    evidence = {"stage": "ready", "head": head, "base": base, "task": repair_task(task),
                "checks": [{"id": c["id"], "name": c["name"], "conclusion": c["conclusion"]}
                           for c in gates.values()], "failures": []}
    for name, check in gates.items():
        if check["conclusion"] == "success":
            if name == "independent-review":
                outcome = json.loads(check.get("output", {}).get("text") or "null")
                if (not isinstance(outcome, dict) or outcome.get("schema") != "rootprint-review-outcome-v1"
                        or outcome.get("kind") != "approval" or outcome.get("head") != head
                        or outcome.get("task") != evidence["task"] or outcome.get("base") != base):
                    return {"stage": "waiting", "head": head, "base": base}
            continue
        if check["conclusion"] != "failure":
            raise ValueError("Current-head check stopped operationally; repair needs actionable evidence")
        if name == "independent-review":
            outcome = json.loads(check.get("output", {}).get("text") or "null")
            if (not isinstance(outcome, dict) or outcome.get("schema") != "rootprint-review-outcome-v1"
                    or outcome.get("kind") != "rejection" or outcome.get("head") != head
                    or outcome.get("base") != base or outcome.get("task") != evidence["task"]):
                raise ValueError("Review diagnostics are legacy, stale, missing or infrastructure-only; no speculative repair")
            result = outcome.get("result")
            # Revalidate shape/length, without trusting source paths as host paths.
            files = [f.get("path") for f in result.get("findings", []) if isinstance(f, dict)] if isinstance(result, dict) else []
            validate_result(result, task, files)
            if result["decision"] != "request-changes" or not any(f["severity"] == "blocking" for f in result["findings"]):
                raise ValueError("Review rejection has no actionable blocking findings; clarification required")
            evidence["failures"].append({"check": name, "result": result})
        else:
            suite = check.get("check_suite", {}).get("id")
            runs = api_items(reader, f"/actions/runs?head_sha={head}", "workflow_runs")
            runs = [r for r in runs if r.get("head_sha") == head and r.get("check_suite_id") == suite
                    and r.get("path") == ".github/workflows/ci.yml" and r.get("status") == "completed"
                    and r.get("conclusion") == "failure"]
            if len(runs) != 1 or suite is None:
                raise ValueError("CI run diagnostics are unavailable or superseded")
            jobs = api_items(reader, f"/actions/runs/{int(runs[0]['id'])}/attempts/{int(runs[0]['run_attempt'])}/jobs", "jobs")
            failed = [j for j in jobs if j.get("conclusion") == "failure" and j.get("name") != "ci"]
            if not failed:
                raise ValueError("CI failure has no complete failed-job diagnostics")
            diagnostics = []
            for job in failed:
                steps = [s for s in job.get("steps", []) if s.get("conclusion") == "failure"]
                # Only baseline verification failures are reproducible source repair input.
                if not steps or any(s["name"] not in ("Run python scripts/check.py", "Run python scripts/package_check.py")
                                    for s in steps):
                    raise ValueError("CI setup/infrastructure failure requires intervention, not source repair")
                match = re.fullmatch(r"https://api\.github\.com/repos/" + re.escape(reader.repo) + r"/check-runs/([0-9]+)",
                                     job.get("check_run_url", ""))
                if not match:
                    raise ValueError("CI job lacks an attributable check-run diagnostic path")
                annotations = bounded(reader.pages(f"/check-runs/{int(match[1])}/annotations"), 100)
                diagnostics.append({"job": job["name"], "steps": steps, "annotations": annotations})
            evidence["failures"].append({"check": name, "run": runs[0]["id"], "diagnostics": diagnostics})
    if evidence["failures"]:
        evidence["stage"] = "repair"
    fingerprint(evidence)
    return evidence


def overlay(client, seed, head):
    """A complete bounded tree delta, including removals, never API patch text."""
    def tree(commit):
        response = client.api("GET", f"/git/trees/{sha(commit)}?recursive=1")
        if response.get("truncated") or len(response["tree"]) > 2000:
            raise ValueError("Repair Git tree is incomplete or oversized")
        result = {}
        for entry in response["tree"]:
            if entry["type"] == "tree":
                continue
            if entry["type"] != "blob" or entry["mode"] not in ("100644", "100755"):
                raise ValueError("Unsupported symlink/submodule in repair source")
            name = entry["path"].rsplit("/", 1)[-1]
            if name.startswith(".env") or name.endswith((".pem", ".key")):
                raise ValueError("Credential-file paths cannot enter repair source")
            if entry["path"] in result:
                raise ValueError("Duplicate repair tree path")
            result[entry["path"]] = entry
        return result

    before, after = tree(seed), tree(head)
    # The trusted image deliberately excludes ambient OpenCode configuration.
    # Import it only as inert sandbox source, never as orchestration configuration.
    paths = sorted(p for p in before.keys() | after.keys() if p.startswith(".opencode/") or
                   (before.get(p, {}).get("sha"), before.get(p, {}).get("mode")) !=
                   (after.get(p, {}).get("sha"), after.get(p, {}).get("mode")))
    if len(paths) > 100:
        raise ValueError("Repair source overlay exceeds 100 files")
    changes = []
    total = 0
    for path in paths:
        entry = after.get(path)
        content = None
        if entry:
            if not 0 <= entry.get("size", -1) <= 1024 * 1024:
                raise ValueError("Repair source file exceeds size limit")
            total += entry["size"]
            if total > MAX_PATCH:
                raise ValueError("Repair source exceeds decoded overlay limit")
            blob = client.api("GET", "/git/blobs/" + sha(entry["sha"]))
            if blob.get("encoding") != "base64" or blob.get("size") != entry["size"]:
                raise ValueError("Invalid repair blob metadata")
            content = blob["content"].replace("\n", "").replace("\r", "")
            if len(content) > 4 * ((entry["size"] + 2) // 3):
                raise ValueError("Repair blob exceeds encoded size limit")
            raw = base64.b64decode(content, validate=True)
            actual = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
            if len(raw) != entry["size"] or actual != entry["sha"]:
                raise ValueError("Repair blob does not match immutable tree")
        changes.append({"path": path, "mode": entry["mode"] if entry else "100644", "content": content})
    if changes:
        validate_changes(changes)
    return {"changes": changes, "tree": {p: [e["mode"], e["sha"]] for p, e in after.items()}}
