# Proposal

## Why

Issue #23 cleared its requirements question but then stopped at “Plan must
reference an OpenSpec contract”: the worker has no supported initial documentation
maintenance route. Its status comments also leave owners guessing whether to
answer, change labels, retry, fix setup or wait for a PR.

## What Changes

- Extend the existing `maintenance` report kind to documentation-only initial
  issues as well as existing-PR repair, retaining separate planning and execution.
- Have the worker select the applicable OpenSpec process contract and record the
  owner's documentation scope plus runnable acceptance; do not require the owner
  to supply internal contract paths or invent a requirement delta/code regression.
- Enforce the same documentation-only output boundary before both publication
  paths; runtime, configuration, executable policy and requirement changes must
  use their proper bug/feature route.
- Include concrete, context-specific “Next step” instructions in issue-state
  comments, covering clarification, `ready`, blocked work, retries, checks, manual
  merging and completion. State when waiting is the correct action.
- Preserve existing authorization, retry limits, isolated verification, App-bound
  checks and owner manual merging.

## Capabilities

### New Capabilities

- `worker-issue-guidance`: Actionable, accurate next-step instructions accompanying
  worker issue-state updates, including documentation-only requests and failures.

### Modified Capabilities

None. Main specs remain empty; bootstrap's unarchived `automated-maintenance`
delta supplies the existing AI-maintenance/issue-lifecycle contract. Documentation
intake is a conformance fix; the owner's explicit next-step guidance requirement
is additive and is specified separately here. This plan does not complete the
unrelated bootstrap activation or automatic-merge requirements.

## Impact

Expected apply targets: trusted worker policy, `scripts/issue_worker.py`, existing
lifecycle/repair tests and worker/setup documentation. Reuse the existing report
schema, state comment and API permissions; no dependency, service or publishing
integration is needed. `preserve-worker-clarification-context` remains a separate
plan on `docs/preserve-clarification-context`; reconcile shared state/policy edits
when applying. This session does not implement the worker or modify issue #23.
