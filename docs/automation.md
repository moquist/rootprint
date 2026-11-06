# Automation activation and operations

## Current status

Run `python scripts/activation.py` for a machine-readable report. It checks the
local origin configuration without printing the remote URL (which could contain
credentials). `--require-active` exits nonzero while autonomy is inactive.

Prepared locally: spec-driven agent instructions, shared verification, a
read-only CI matrix, issue forms, weekly Dependabot configuration, and an
[issue worker](issue-worker.md) with isolated OpenCode execution, and a tool-free
[independent reviewer](independent-review.md). **No
unattended issue worker, independent PR reviewer, auto-merger, release bot, or
publisher is verified as running.** The worker is disabled by default and needs
controlled hosted verification. The reviewer is also disabled by default and
awaits App/OpenAI/check-enforcement acceptance. Merge and release integrations
still need implementation and live verification. The owner reports that CI passed
after pushing the worker; that does not activate autonomous maintenance.

## What local operation gives up

AI can implement and verify changes during interactive sessions. It is not
listening for reports or repairing failures while no agent session is running.
During interactive local work, the owner performs every push. Agents prepare
verified local commits and owner-run commands; they must not push or request
push credentials. GitHub-settings authorization does not authorize pushing.
`docs/local-work.md` substitutes for an issue ledger until GitHub is available.
The owner has now pushed and reports successful hosted CI. Recorded local test
results remain separate from that owner report. GitHub event delivery, hosted
worker/reviewer isolation, App permissions, and merge enforcement still need a
controlled acceptance run with recorded links.

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
