# Automation activation and operations

## Current status

Run `python scripts/activation.py` for a machine-readable report. It checks the
local origin configuration without printing the remote URL (which could contain
credentials). `recordedHostedEvidence` identifies dated observations for
`moquist/rootprint`: the hosted CI matrix, reviewer App approval, manual issue
lifecycle and merge rules. These remain historical evidence even in a checkout
without an origin, or with a different origin. `liveRemoteChecksPerformed` is
`false`: the command makes no GitHub/provider request and does not read credentials.
`--require-active` exits nonzero while autonomous maintenance is unverified.

Hosted evidence as of 2026-11-07 confirms cross-platform CI, separate-App
[independent review](independent-review.md), no-bypass App-bound merge gates and
the [issue worker](issue-worker.md)'s documentation issue-to-PR-to-manual-merge
path. See [the ledger](local-work.md) for exact heads, check IDs, runs and limits
of that evidence. Remaining acceptance includes hostile input, repeated events,
exhausted attempts/recovery, failure deduplication and a failing bug regression.
Automatic merging and release integrations still need implementation and
verification; the last inspected repository settings had auto-merge disabled.

## What local operation gives up

AI can implement and verify changes during interactive sessions. A local session
does not run an unattended daemon; deployed GitHub workflows operate separately.
During interactive local work, the owner performs every push. Agents prepare
verified local commits and owner-run commands; they must not push or request
push credentials. GitHub-settings authorization does not authorize pushing.
`docs/local-work.md` preserves local handoffs and hosted acceptance evidence;
GitHub issues and App-authored state comments track deployed worker outcomes.
Recorded local results and historical hosted observations do not establish
current service health or completion of the remaining bootstrap scenarios.

These are activation gaps, not permission to weaken the specified gates.

## Activation sequence

1. Owner selects GitHub repository visibility and performs all local-work pushes.
   The agent does not create a public repository or publish implicitly.
2. Confirm the `CI` workflow runs on all configured hosts. The stable aggregate
   required check is **`ci`**; it fails if any matrix job fails or is skipped.
3. Implement and install a dedicated GitHub App for issue comments, branch/PR
   writes, check results, and merge operations. Use App-generated PRs so normal
   CI events are triggered. Scope its installation to this repository.
   The initial worker is now implemented; configure its App and OpenAI secrets
   using [the worker guide](issue-worker.md). It opens PRs without merging them.
4. Connect OpenCode model access in trusted orchestration. Keep provider
   credentials outside credential-free code-execution sandboxes, and verify
   that isolation with adversarial issue content. Do not simply run an
   unrestricted agent shell beside write/publishing credentials.
5. Configure the implemented fresh-context automated review producing **`independent-review`**
   on the exact PR head SHA. The reviewer reads diffs as untrusted data, without
   executing PR code. New commits invalidate prior review/check evidence. Follow
   [the reviewer setup guide](independent-review.md) to install the separate App,
   enable a controlled run, and verify its check source.
6. Configure a no-bypass branch ruleset requiring `ci` and `independent-review`,
   with normal human PR approval not required. Never temporarily drop the review
   requirement to make a not-yet-integrated bot merge.
7. Verify one controlled issue-to-spec-to-fix-to-review-to-merge run. Enable
    unattended issue schedules and auto-merging only after that evidence exists.
   During the initial rollout, use owner-applied `ready` labels and a manual merge
   after the same required checks pass. Verify automatic merging separately when
   the owner chooses to enable it.

## Worker contract

State labels: `triage`, `needs-information`, `ready`, `in-progress`, `blocked`,
`done`. Triage links likely duplicates with evidence. Missing reproduction or
material ambiguity produces a focused issue question. Each accepted issue links
its OpenSpec contract and PR; each failure links its run and evidence.

Plan, apply, and archive are separate phases. Existing-contract bugs require a
failing regression check before the fix, not an invented new requirement.
Workers must inspect all callers and keep ports and vectors compatible.
An independent reviewer checks acceptance scenarios, error paths, protocol
compatibility, and automation trust boundaries before approving the latest SHA.

Enforce one worker per issue and a 30-minute run timeout. Persist attempt counts
per issue revision; stop after three failed implementation attempts. Reopening
without new information must not silently reset an exhausted budget. New issue
information or an explicit eligible retry can unblock it. Failure tracking must
deduplicate rather than opening one issue per repeated CI failure.

## Releases and rollback

Current local package checks build and install both distributions:
`python scripts/package_check.py`. This is not publication. EPL-2.0 is selected
and included in both distributions. Configure npm/PyPI ownership and publishing
identity before enabling releases.

The specified release integration creates a version/release-note PR, merges it
through normal gates, builds both distributions from the verified default-branch
revision, and publishes once. Package versions are independent of `rootprint-v1`.
Record partial failures and retry only missing registry artifacts. Never
overwrite an existing version or change published protocol bytes in place.

Rollback: disable worker/merge/release triggers, preserve issue/run evidence,
revert the bad change through verified CI, and release a new package version if
needed. Routine human code edits or routine human PR review are not required.
