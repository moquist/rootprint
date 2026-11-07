# Design

## Context

See `proposal.md` for motivation. Bootstrap's unarchived `automated-maintenance`
delta supplies the baseline. Main specs are empty. The new additive capability
does not complete bootstrap's automatic-merge or broader hosted acceptance tasks.

Observed implementation:
- `Worker.execute()` returns through `check_pr()` whenever durable state has a
  PR; failures only set `blocked`. `/rootprint retry` is processed later and
  therefore does not currently resume existing-PR work.
- Attempts and run links live in one App-authored issue comment. Issue revision
  excludes bot comments and the explicit retry command; `save()` consumes `ready`.
- Check observation currently reads one page, combines failures by name, and does
  not establish App identity, complete evidence or readiness from required checks.
- `publish()` parents initial commits on trusted host HEAD; `Sandbox` seeds source
  from the default-branch-built image. Neither supplies an existing PR baseline.
- The reviewer publishes validated findings as rendered check summaries, while
  provider/context failures also conclude `failure`. These need a typed distinction.
- Existing tests exercise initial publication, budgets, hostile patch rejection
  and lost PR-create responses. The workflow already serializes per issue and
  reconciles CI completions and scheduled runs; reviewer outcomes can be picked
  up by scheduled reconciliation without introducing another orchestration service.

## Goals / Non-Goals

**Goals:** Extend the existing worker with one bounded repair path, preserving
its trusted coordinator, isolated phases, attempt ledger and manual-merge rollout.

**Non-Goals:** Repair arbitrary/fork PRs, enable automatic merging or issue selection,
publish packages, rewrite branch history, add a queue service, inspect image
contents in review, or automatically broaden requirements to satisfy feedback.

## Decisions

### 1. Reconcile existing PRs using the current issue state

Keep per-issue concurrency and the existing scheduled/CI-triggered discovery.
Persist the issue revision for which `ready` authorized implementation and repair,
alongside the worker PR/repository/branch identity. Initial publication and repair
share `attempts[authorized_revision]`. For old PRs without this field, monitor but
require a fresh owner `ready` or permission-checked `/rootprint retry` to adopt the
repair scope; do not infer consent from the presence of an old PR alone.

Process scope changes and authorized retries before the existing-PR early return.
New issue information pauses until renewed authorization. Reopening/relabeling
unchanged information does not reset attempts; explicit eligible retry retains
the existing reset semantics. PR comments are repair context, not a way to reset
the issue budget. This avoids a second repair counter that could multiply retries.

Persist a reservation with revision, head/base, failure fingerprint, attempt and
run before the model runs. A completed/no-change/blocked attempt is not replayed
for identical evidence. An interrupted attempt remains consumed; reconciliation
can use the next available attempt after establishing no pending publication.

### 2. Collect bounded diagnostics as untrusted data

Use paginated current-head check/status evidence, expected CI/reviewer App IDs
and the required gate names. Ignore obsolete results and wait for pending checks.
Read CI failure diagnostics through fixed GitHub API operations; never execute a
log command or follow a diagnostic-supplied URL on the host. Use the workflow's
read-only token with explicit Actions/check read permissions for diagnostic reads;
keep App writes scoped as today. No reviewer private key enters the worker.

Add bounded machine-readable review outcome data to check output, distinguishing
validated rejection/findings from infrastructure/context errors and tying it to
the reviewed head/base. Keep existing human summaries and merge gates. Legacy
prose-only failures are not guessed into actionable rejections.

Bound the combined serialized task/diagnostics to the existing 90,000-character
worker context ceiling and bounded API reads. Oversized, truncated, missing or
unrecognized evidence blocks with links rather than silently dropping necessary
findings. Provider errors and unavailable dependencies are operational blockers;
triage can ask for clarification when evidence does not define an actionable fix.

### 3. Seed the exact PR head without executing it on the host

The image and orchestration still come from trusted default-branch source.
Retrieve immutable Git tree/blob data for the diagnosed PR head and the seed
revision. Build a complete bounded overlay, including deletions and modes, using
the existing 100-file/1-MiB-file/4-MiB-patch validation limits. Refuse unsupported
paths/modes, symlinks, truncated trees or overlays beyond those limits.

Transfer validated regular-file data only into the disposable container; establish
the resulting source as its local patch-export baseline before any model phase.
Verify its tracked tree corresponds to the expected PR snapshot. Trusted bridge
and policy remain outside that writable source. Do not extract untrusted archives
onto the host or build a privileged image from PR Dockerfiles. Offline baseline
dependencies remain the ceiling; incompatible new dependency requirements block.

Reuse separate plan/implement/complete phases and final verification. Code bugs
need a failing-before/passing-after regression; non-code findings use appropriate
acceptance checks without inventing a fake regression. Clarified new behavior
needs the usual OpenSpec planning before implementation.

### 4. Append and recover, never overwrite

Create the repair tree relative to the diagnosed PR head and parent the repair
commit on that exact head, not host HEAD. Re-read issue revision, PR state/identity,
head/base and latest failure evidence after verification and before publishing.
If they differ, discard the stale result and report why.

Persist the commit-create intent (tree, parent, message and fixed author/committer
timestamps), then the candidate commit and expected branch parent before the
non-force ref update. Retrying identical commit creation after a lost response
must yield the same Git object rather than a second repair. A concurrent sibling
commit makes fast-forward publication fail rather than lose owner work. After a
lost response, inspect the actual branch and pending
identity: recognize the candidate (including when retained in later branch history),
retry only a still-applicable ref write, or block a conflicting head. Never rerun
the model merely because an already-successful publication response was lost.
No second PR and no force update are fallback mechanisms.

### 5. Report readiness, leave the merge to the owner

Use the existing lifecycle labels, with a durable stage/message distinguishing
repair, waiting for checks and ready for owner merge within `in-progress`.
Readiness requires both current-head expected-App gates to succeed; a lack of
failed checks is insufficient. App-generated commits trigger ordinary CI/review.
No merge API, auto-merge mutation, self-approval or repository-setting mutation is
part of this change. Closing the issue/PR stops work; only an observed merge is done.

## Risks / Trade-offs

- Repeated or delayed events → one reservation/publication record and existing
  per-issue serialization; recover pending writes before spending another attempt.
- Diagnostic prompt injection → diagnostics remain bounded task data; source/test
  execution stays offline without provider/write credentials or host mounts.
- Owner edits during work → recheck all input identities and use non-force child
  commits; fail closed on divergent history instead of rebasing or overwriting.
- Large PR/seed drift → bounded overlay can block; report its actual limit rather
  than add an unrestricted fetch/extraction path.
- Historical evidence mistaken for deployment → local and hosted tasks remain
  separate, with real run/check/head links required for activation claims.

## Migration Plan

1. Implement and verify locally in a separate apply phase. Keep all implementation
   and hosted tasks unchecked until their specified checks actually pass.
2. Owner publishes through current-head CI and independent review, then manually
   rebase-merges. Any read-permission changes must be explicit in the workflow.
3. Exercise one controlled worker PR: actionable failure, automatic repair on the
   same PR, fresh CI/review, and an open PR awaiting owner merge. Exercise bounded
   retries, duplicate events, hostile diagnostics and stale-head recovery as well.
4. Record exact hosted evidence before claiming repair activation. Keep auto-merge
   disabled. Roll back by disabling the worker/cancelling active runs and reverting
   through normal gates, preserving durable state and attempt history.
