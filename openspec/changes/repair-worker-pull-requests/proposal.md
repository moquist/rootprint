# Proposal

## Why

The issue worker currently stops at a blocked existing PR when CI or independent
review fails, so completing an authorized issue still requires interactive repair.
Bounded repairs on that PR should carry work through fresh verification while
leaving the owner in control of the final rebase merge.

## What Changes

- Extend an issue's initial `ready` authorization to bounded repairs of its
  existing worker PR, using the same three-attempt budget as initial implementation.
- Reconcile actionable current-head CI failures and independent-review rejections,
  collect bounded diagnostics, and pause on infrastructure failures or ambiguity.
- Plan, implement and verify repairs in the existing credential-free sandbox,
  then append a commit to the same branch without overwriting intervening edits.
- Persist failure/attempt/publication identity so repeated events and interrupted
  runs cannot duplicate repairs or reset their budget.
- Require fresh CI and independent review on each repaired head, then wait for
  the owner's manual merge. Do not enable automatic merging or publishing.

## Capabilities

### New Capabilities

- `pull-request-repair`: Authorized, bounded, isolated repairs to existing worker
  PRs, with durable recovery, current-head checks and manual owner merge.

### Modified Capabilities

None. Main specs are empty; unarchived bootstrap's `automated-maintenance` delta
is the applicable baseline. This additive capability retains its credential,
retry, verification and rebase-only constraints. It describes the manual-merge
rollout; bootstrap's later automatic-merge requirement remains incomplete and
is not removed or activated by this change. Synchronize the baseline before
archiving dependent changes.

## Impact

Expected implementation areas: `scripts/issue_worker.py`, `worker_sandbox.py`,
`worker_agent.py`, `independent_review.py`, their existing tests, trusted worker
policy, workflow read permissions and operational/activation documentation.
Hosted acceptance requires owner deployment through ordinary CI and independent
review. No package API, protocol bytes, conformance vectors, dependency or registry
change is intended. This proposal authorizes planning only.
