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
| Variable | `ISSUE_WORKER_ENABLED` | Leave unset/`false` until ready for a controlled run; set `true` to run the worker |

Install the implementation App on this repository only, with metadata read and
contents/issues/pull-requests read/write permissions. It needs no bypass,
administration, publishing, or reviewer credentials. The coordinator creates a
repository-scoped installation token and revokes it at the end of the run. The
reviewer App's key is not referenced anywhere in this worker workflow.

Keep the default Actions token read-only. The worker uses OpenCode **1.19.4** and
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

## Durable state and retries

One App-authored issue comment stores the current state, revision hashes, attempt
counts, run links, and any PR/publication recovery data. Do not edit/delete that
comment: missing durable history cannot establish an accurate attempt budget.
Lifecycle labels are `triage`, `needs-information`, `ready`, `in-progress`,
`blocked`, and `done`; other labels are preserved.

Each revision allows at most three implementation attempts. Revision identity
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
or a PR closed without merging produce `blocked`. An existing PR is monitored,
not silently replaced by a second implementation PR. Further repairs to an open
PR are not currently driven by this issue worker.

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
