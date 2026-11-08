# Proposal

## Why

Issue #23 repeats a clarification despite the owner answering it: model context
keeps the short human reply but drops the worker's preceding question. The next
run also overwrites the question-bearing state message before building context.

## What Changes

- Preserve clarification questions in the existing durable App-authored issue
  state, surviving status updates, restarts and multiple clarification rounds.
- Supply those questions alongside human answers to resumed triage and downstream
  phases, including existing-PR repair, within the existing input/state limits.
- Recover a legacy question when it is still present in a needs-information state;
  do not fabricate questions whose original text has already been lost.
- Add regression coverage for the short-answer round trip, trust boundaries,
  bounded context, deduplication and unchanged authorization/attempt accounting.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

None. This is a conformance bug fix for bootstrap's existing `Automated issue
lifecycle`, `Untrusted input and credential isolation` and `Bounded observable
automation` requirements in
`openspec/changes/bootstrap-rootprint-ecosystem/specs/automated-maintenance/spec.md`.
Main specs remain empty. `skip_specs: true` records that no requirement delta is
needed; the fix must restore meaningful clarification/resumption, not invent new
behavior or infer implementation authorization from conversational agreement.

## Impact

Expected edits during apply: `scripts/issue_worker.py`, existing lifecycle/repair
tests, trusted worker policy and worker operations documentation. Reuse the current
state comment, scoped API client, sandbox and per-phase 90,000-character guard.
No new dependency, service, permission, protocol or package API is needed.
The owner handles #23's workaround separately; this session plans the worker fix only.
