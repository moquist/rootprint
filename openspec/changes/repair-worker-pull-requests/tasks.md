# Tasks

## 1. Durable authorization and repair attempts

- [x] 1.1 Extend existing worker state and reconciliation to persist authorized issue revision and worker PR/branch identity; process existing-PR authorization/retry before the early return. Verify tests for initial `ready` covering bounded repairs, legacy PRs requiring explicit authorization, changed issue scope, draft/closed/foreign PRs and unchanged reopen/relabel behavior. Update worker policy and `docs/issue-worker.md` with those authorization rules.
- [x] 1.2 Add durable repair reservations/failure fingerprints using the existing shared attempt counter and per-issue serialization. Verify initial implementation plus at most two repairs, exhaustion, authorized retry, repeated scheduled/events, completed/no-change attempt deduplication and interrupted attempts consuming their reservation. Document recovery and stop conditions beside the lifecycle tests.

## 2. Actionable failure evidence

- [x] 2.1 Add bounded machine-readable current-head/base outcome data to independent-review check output distinguishing validated rejection from infrastructure/context failure while preserving human summaries and existing gates. Verify reviewer tests for actionable findings, provider errors, malformed/missing legacy output and freshness; update reviewer documentation for the diagnostic contract.
- [x] 2.2 Collect paginated latest CI/reviewer evidence and bounded diagnostics through fixed read-only API operations with explicit workflow Actions/check read permissions. Verify tests for expected App attribution, superseded/stale/pending/missing/spoofed results, operational failures, truncation and the 90,000-character total context ceiling; confirm no arbitrary diagnostic URL/command execution or credential leakage. Update workflow/setup documentation with the actual read permissions and failure classifications.

## 3. Exact-head sandbox and phased repair

- [x] 3.1 Add safe immutable PR-head overlay import into the existing sandbox with its patch-export baseline set to that snapshot. Verify a real credential-free runtime check preserves prior PR additions/deletions/modes and exports only subsequent repair changes; test mismatched snapshots, unsupported paths/modes/symlinks, truncated trees and existing size limits. Document offline dependency and overlay ceilings.
- [x] 3.2 Connect actionable existing-PR failures to separate plan, implementation and completion phases under the trusted worker policy. Verify lifecycle tests for a meaningful failing-before/passing-after bug regression, non-code acceptance evidence, ambiguity pausing, hostile diagnostics, failed verification preventing publication and integrated/package checks on the exact completed tree. Update the policy and worker guide to describe repair evidence without granting new host tools or credentials.

## 4. Non-overwriting publication and owner merge

- [x] 4.1 Append repairs to the existing branch using the diagnosed head as parent and non-force ref updates after rechecking issue revision, PR identity/state/head/base and latest applicable failure. Verify tests for the same PR/branch, unchanged existing content, owner edits, base movement, superseded failure evidence and publication races; document conflicts as explicit blocked outcomes rather than force/rebase fallbacks.
- [x] 4.2 Persist deterministic commit-create intent and pending ref publication; reconcile lost commit-create/ref-update/state-save responses against actual branch history before starting more model work. Verify recovery tests produce one repair commit on the existing PR, preserve divergent owner commits and do not reset attempts or create another PR; document interrupted-publication recovery.
- [x] 4.3 Distinguish repairing, waiting for required checks and ready for owner merge in the existing issue record. Verify tests for fresh expected-App CI/review on each new head, old approval not carrying forward, missing/pending/failing gates withholding readiness, manual merge recording done, and closure without merge blocking work. Assert no merge/auto-merge/self-approval/settings-write calls. Update activation reporting, README automation text and setup/worker guidance, keeping usage/setup/all-tests examples current.

## 5. Integrated verification and hosted acceptance

- [x] 5.1 Run credential-free `python3 scripts/check.py`, `python3 scripts/package_check.py`, applicable sandbox/runtime checks, Actionlint for changed workflows, `node_modules/.bin/openspec validate --all --strict` and `git diff --check`. Review the complete affected flow and diff; record actual commands/results and remaining deployment gates in `docs/local-work.md` before committing intended changes.
- [ ] 5.2 After owner deployment through ordinary current-head CI and independent review, exercise a controlled worker PR that automatically repairs actionable CI failure and reviewer rejection on the same PR. Record exact issue/run/head/check evidence for failing-before/passing-after regression, new-head CI/review and the passing PR remaining open for owner approval; verify owner rebase merge is followed by accurate done status. Do not mark this hosted task complete from local mocks or publication alone.
- [ ] 5.3 Record controlled hosted evidence for duplicate reconciliation without duplicate repair, exhausted shared attempts stopping, infrastructure/hostile diagnostics failing closed, intervening owner-head changes preserving edits and interrupted publication recovery. Verify no merge/auto-merge operation was requested and repository auto-merge remains disabled; keep unexercised scenarios explicitly open.

## Workflow follow-up

- Obtain independent automated review before any remote merge; the owner performs interactive local pushes and final manual rebase merges.
- Leave bootstrap's unrelated activation/automatic-merge/release requirements open; repair planning and local checks do not complete them.
- Archive/synchronize through the archive workflow only after acceptance and baseline synchronization prerequisites are satisfied, then verify resulting specs.
