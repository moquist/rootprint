# Issue worker: setup and operation

The initial implementation prepares PRs for **manual merging**. It does not merge,
enable auto-merge, approve its own PRs, or publish packages. The
[independent reviewer](independent-review.md) is implemented separately and needs
owner activation plus hosted verification. Keep `ci` and
`independent-review` required before merging any worker PR.

## Configure GitHub

The workflow is `.github/workflows/issue-worker.yml`. It reads orchestration code
only from the repository's default branch, never from an issue-supplied branch or
a PR checkout. Push/install this verified implementation only with owner
authorization. This document does not attest that hosted automation is active.

Under **Settings → Secrets and variables → Actions**, configure:

| Kind | Name | Value |
| --- | --- | --- |
| Secret | `IMPLEMENTATION_APP_PRIVATE_KEY` | Complete implementation App PEM private key |
| Secret | `OPENAI_API_KEY` | OpenAI API key with access to GPT-6.1 Sol |
| Variable | `IMPLEMENTATION_APP_ID` | Implementation App's App ID, not Client ID |
| Variable | `REVIEWER_APP_ID` | Separate reviewer App ID; required for repair evidence attribution |
| Variable | `ISSUE_WORKER_ENABLED` | Leave unset/`false` until ready for a controlled run; set `true` to run the worker |

Install the implementation App on this repository only, with metadata read and
contents/issues/pull-requests read/write permissions. It needs no bypass,
administration, publishing, or reviewer credentials. The coordinator creates a
repository-scoped installation token and revokes it at the end of the run. The
reviewer App's key is not referenced anywhere in this worker workflow.

Keep the default Actions token read-only. The workflow's ephemeral token has explicit
contents/issues/PR/checks/Actions read permissions for repair evidence. It receives
no reviewer private key or new App write scope; do not substitute a repository-write
token. The worker uses OpenCode **1.19.4** and
model **`openai/gpt-6.1-sol`**. Catalog recognition is checked without a real key;
actual OpenAI API availability, entitlement, billing, and rate limits must be
verified in the controlled hosted run. Configure provider spending controls in
the OpenAI account. GitHub-hosted runners and OpenAI usage are separate costs.

The existing Actions allowlist (`actions/checkout`, `actions/setup-node`, and
`actions/setup-python`) also covers this workflow. No additional action is needed.

## First controlled run

1. Confirm hosted `ci` succeeds. Configure the no-bypass merge gates and the
   independent reviewer before merging worker PRs; its App credentials and enabled
   workflow remain separate activation prerequisites.
2. Enable the worker with `ISSUE_WORKER_ENABLED=true`. This enables report triage
   and scheduled reconciliation; it does **not** authorize implementation of
   every issue.
3. Open one small, reproducible issue. Triage should identify its contract,
   request missing information, or link likely duplicates. An actionable report
   waits for you to apply `ready`.
4. Apply `ready`. The worker consumes that authorization, records its attempt,
   separately plans and implements the work, runs checks, and opens a linked PR.
5. Verify the issue's durable state comment, regression evidence, plan links, PR,
   current-head CI, and independent automated review. You click **Merge**.
6. The next reconciliation records the merge outcome and marks the issue `done`.
   Record hosted evidence in `docs/local-work.md` before claiming activation.

For a missed event, use **Actions → Issue worker → Run workflow**, supplying the
issue number. `0` reconciles all candidate issues. Events cover issue creation,
reopening, edits, labels, and non-bot comments. Reconciliation runs every 30 minutes
(GitHub may delay scheduled jobs). It also monitors worker PRs for current-head
failures and deduplicates default-branch CI failures into one tracking issue.

## Documentation-only requests and issue prompts

The locally implemented documentation route and prompts await controlled hosted
acceptance. A wording-only issue can use `maintenance` in both initial work and
repair. The worker selects the existing main `automated-maintenance` process spec,
or bootstrap's delta while main is absent; the owner supplies prose requirements,
not internal contract paths. Planning records targets, intended edits and a runnable
post-edit acceptance command in `regression`. It need not fail before the edit or
create a new spec delta. Separate plan/implement/complete phases and integrated/
packaged checks still run. Example issue: “In README.md, explain that calculatedAt
is metadata; keep runtime behavior unchanged.” The worker can accept it with a
short Python assertion over the requested wording after editing.

Maintenance can change root `README.md`, `github-automation-setup-instructions.md`,
the Python/TypeScript package `README.md` files, and `.md`/`.txt`/`.rst` prose under
`docs/`. Every file must remain regular and non-executable. Code, tests, package/
workflow configuration, `AGENTS.md`, `automation/` policies, `.opencode/` instructions
and normative OpenSpec artifacts are excluded. The complete exported diff is
checked after completion, for both initial and repair publication. Behavior or
requirement changes need their proper bug/feature route even when phrased as prose.

Each state update has a separate **Next step** section, for example “Add the
`ready` label to authorize an attempt” or “Request a worker planning/scope fix …
before retrying.” It is trusted procedural guidance, not a retained question or
an owner answer. It cannot grant authorization or reset attempt/review budgets.

| Stage/reason | Owner action in the issue |
| --- | --- |
| Active triage/implementation/repair | Wait and follow the run link; no extra readiness action. |
| Needs information | Answer the focused question here. Replies are re-triaged; add `ready` once scope is confirmed. Label cleanup is automatic. |
| Actionable, waiting for authorization | Add `ready`; it consumes an attempt without resetting the budget. |
| Setup/provider/permission/dependency/runner blocker | Resolve the named prerequisite first; follow diagnostics, then resume through the indicated workflow. |
| Invalid worker plan or documentation scope | Request a worker fix before retrying; do not supply internal paths or relabel unchanged defective work. |
| Investigated failure, budget remaining | Resolve its cause, then add `ready` for initial work; use the linked run/workflow if an event was missed. |
| Attempts or triage failure limit reached | Material new information with renewed readiness, or an explicit `/rootprint retry` by a write/maintain/admin collaborator. Reopening/relabeling alone cannot reset the limit. |
| PR gates pending | Wait for current-head `ci` and `independent-review` on the linked PR. |
| PR check infrastructure failure | Fix setup first; rerun affected CI or dispatch Independent review with the PR number and `retry` enabled, then reconcile Issue worker with the issue number. Review retry limits still apply. |
| PR gates pass | Review the linked PR and use **Rebase and merge**; no new `ready`. |
| PR closed without merge | Resolve its disposition, e.g. reopen it; no automatic replacement PR. |
| Merged/done | No further implementation action for this work. |

Identical status/reason/action saves reuse the one comment without rewriting it
merely for a new run link. Guidance counts against the 60,000-character state limit.
If comment access or capacity prevents publication, the worker fails with Actions
diagnostics; it does not claim to have delivered a prompt. Keep required CI/review
gates and manual merging in place throughout rollout.

## Durable state and retries

One App-authored issue comment stores the current state, revision hashes, attempt
counts, run links, and any PR/publication recovery data. Do not edit/delete that
comment: missing durable history cannot establish an accurate attempt budget.
Lifecycle labels are `triage`, `needs-information`, `ready`, `in-progress`,
`blocked`, and `done`; other labels are preserved.

Clarification questions are retained in that same App-authored state record across
generic status updates, restarts, retries and existing-PR repairs. Each records its
issue revision, worker run and the last observed human comment ID; human answers
remain native issue comments. Models receive the complete human discussion with
IDs/authors plus ordered question history and its worker/state-comment provenance.
All of it is untrusted task evidence, including prior worker text: agreement can
resolve a question but cannot authorize implementation, tools, retries or merging.

Legacy state remains readable. A still-present `needs-information` message is
retained before overwrite, with unknown original revision/comment position. An
already-erased question is not reconstructed; supply the missing context explicitly.
Do not edit the state to manufacture history. Malformed history stops processing.
The complete state comment is capped at 60,000 characters; an oversized candidate
cannot replace the last valid record. The worker reports a state-capacity failure
in its run if it cannot save even a bounded blocker. Human replies and questions
are never silently clipped to fit: the complete serialized task must fit 90,000
characters at every model phase, including prior reports and verification text.
Overflow blocks work with a context-limit diagnostic; resolve the issue's scope/
discussion size before retrying rather than increasing budgets implicitly.

Each revision allows at most three implementation attempts. Revision identity
and its initial `ready` authorization cover both implementation and bounded repairs
on its existing worker PR; commits/check reruns do not reset the budget. New issue
information requires renewed authorization. Legacy PRs lacking a recorded repair
authorization need `ready` or an eligible `/rootprint retry`. Repair reservations
and run links are written before model execution; interrupted attempts count, and
completed/no-change attempts are not repeated for identical failure evidence.
Implementation and repairs share that single budget. Revision identity
includes the issue title/body and non-bot information comments. Reopening or
relabeling an unchanged issue does not reset its exhausted budget, nor does an
unauthorized retry command. A user with repository write/maintain/admin permission
can comment **`/rootprint retry`** to explicitly authorize a fresh budget and
attempt. New information resumes triage; apply `ready` again to authorize work
after a pause or failure.

The workflow serializes runs for each issue without cancelling an active worker.
An interrupted implementation consumes its reserved attempt; reconciliation can
resume with the next attempt. A lost branch/PR-create response is reconciled
from the stored commit and branch without rerunning the model or overwriting an
existing branch. A PR awaiting review/merge remains `in-progress`; failing checks
or a PR closed without merging can produce `blocked`. After deployment an existing
PR can be repaired on the same branch within its shared attempt budget; it is never
silently replaced by another PR.

### Existing-PR repairs

The locally implemented repair path awaits controlled hosted acceptance. It reads
latest exact-head `ci` from GitHub Actions App `15368` and `independent-review`
from `REVIEWER_APP_ID`. Missing/pending/stale/spoofed gates do not authorize work.
Once both finish, an actionable failure can trigger separate repair triage, plan,
implementation and completion phases. Code bugs require a real failing-before/
passing-after regression; non-code maintenance requires a runnable acceptance check.

CI diagnostics are complete failed verification-step records and check annotations
for the matching CI run attempt, not privileged log execution or downloaded PR
artifacts. Only `python scripts/check.py` and `python scripts/package_check.py`
step failures are source-repair candidates; the sandbox must reproduce the problem.
Setup/dependency/runner/provider failures, missing or oversized diagnostics and
unclear requirements pause for intervention. Review infrastructure errors and
legacy prose-only failures cannot masquerade as actionable blocking findings.
The combined task/diagnostics ceiling is 90,000 serialized characters, checked
again at every actual model phase after adding prior reports and verification text.
All matrix jobs must be completed with success or source failure before repair;
mixed source failures and operational/unfinished/unsupported outcomes pause work.

Immutable PR Git blobs are overlaid inside the credential-free sandbox and checked
against the complete diagnosed tree. The overlay retains the 100-file, 1-MiB-file,
4-MiB-decoded limits; incomplete/unsupported trees or unavailable offline dependencies
block. `.opencode` source is inert sandbox data, never host/model configuration.
The trusted image, bridge and policy still come from default-branch orchestration.

Verified repairs append a child commit through non-force branch updates. Owner
head/base/issue/discussion/check changes invalidate stale work. Commit-create intent
and pending branch publication survive lost responses; reconciliation recognizes
an already-published candidate, including in later branch history, without another
model attempt. Divergent owner work blocks publication rather than being overwritten.
Once fresh CI/review pass, state says ready for owner manual rebase merge; no merge,
auto-merge, self-approval or repository-setting write is requested.

Jobs have a 30-minute limit; model/verification work shares a 22-minute budget.
Sandbox tool commands have a 90-second limit and coordinator verification
commands a maximum of five minutes. Triage infrastructure failures also stop
after three failures per revision. Provider/runtime logs are not copied into
issues or Actions output; the state comment reports a bounded failure category
and trusted diagnostic, without credential values.

## Execution boundary

- A fresh OpenCode process runs each phase in a private, empty host directory,
  with ambient project/global configuration and external plugins/skills disabled.
  Built-in tools and subagents are denied. Only `sandbox_run` and `sandbox_report`
  are allowed, through the fixed trusted stdio MCP bridge.
- Only OpenCode receives the OpenAI key. It receives no GitHub App key/token.
  The MCP bridge is launched with a cleared environment and fixed runtime,
  container, and result-file arguments. Model input cannot select host paths,
  containers, host commands, or GitHub API endpoints.
- Code and tests run as a non-root user inside a read-only container with dropped
  capabilities, no network, resource limits, writable temporary work directories,
  and **no host mounts, Docker socket, provider credentials, or write tokens**.
- Image preparation installs the baseline dependencies before worker secrets are
  supplied. Execution uses offline npm and Python caches. New dependency needs
  can block a task; the worker must not turn networking or credentials on to
  work around that limit.
- The coordinator collects bounded regular-file changes as data, rejects
  symlinks, traversal, duplicate paths, unsupported modes, and oversized output,
  and creates Git blobs/trees/commits through fixed API operations. It does not
  apply or execute a patch on the host. PR code still needs ordinary read-only CI
  and independent review on its exact head SHA.

Container isolation is a practical VM-hosted execution boundary, not proof that
all possible container/kernel vulnerabilities are absent. Hosted verification is
still required. An App without Workflows write permission cannot publish changes
to `.github/workflows/`; such work can stop with an API failure rather than
silently expanding its permissions.

## Reproduce checks locally

The standard README setup and `python scripts/check.py` include the offline unit
checks for lifecycle, attempts, recovery, and hostile patch input. On Linux with
Docker and `opencode` 1.19.4 on `PATH`, additionally run:

```sh
python3 scripts/worker_sandbox.py build
python3 scripts/worker_runtime_check.py
```

For rootless Podman, use:

```sh
python3 scripts/worker_sandbox.py build --runtime podman
python3 scripts/worker_runtime_check.py --runtime podman
```

The image builder includes Git-tracked working-tree source, so new worker files
must be staged before a local build. It excludes `.opencode`, private-key files,
and `.env` files, and sends no `.git` directory or host caches. These commands
exercise the real sandbox, hostile symlink rejection, pinned OpenCode config,
actual MCP startup, and integrated/package checks with networking disabled. They
need no real GitHub or OpenAI credential and do not spend model tokens.

Limits: at most 200 candidate issues per reconciliation, 100 changed files,
1 MiB per file, and 4 MiB decoded patch contents. Stop and explicitly revise the
deployment if those limits become relevant; no speculative queue service is
required for this repository today.

To stop new runs, set `ISSUE_WORKER_ENABLED=false` or disable the workflow. Cancel
any already-active runs explicitly; changing the variable does not stop an
existing job. Preserve state comments and run evidence. Auto-merge remains
disabled throughout this rollout.
