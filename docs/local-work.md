# Local work ledger

## Hosted acceptance — 2026-11-08 (issue #29 / PR #30)

- Owner confirmed the controlled test worked. Independently inspected fresh issue
  https://github.com/moquist/rootprint/issues/29, comment history/timeline, worker
  runs, complete PR diff, exact-head App checks and owner merge. Prepared local
  `docs/worker-hosted-acceptance` from merged main `f14dfc8`; no remote mutation,
  workflow dispatch, model request, push or merge was performed by this session.
- Question run https://github.com/moquist/rootprint/actions/runs/42440662665 asked
  for confirmation of exact calculatedAt wording/placement. The durable App comment
  https://github.com/moquist/rootprint/issues/29#issuecomment-6716441657 retains the
  complete question, original revision/run and human cursor. The owner's short
  https://github.com/moquist/rootprint/issues/29#issuecomment-6716465117 reply was
  “Your suggestion is great; proceed as proposed.” at 03:01:22 UTC. No self-contained
  restatement or repeated clarification was needed.
- GraphQL issue timeline confirms owner `ready` at 03:01:28, before reservation
  at 03:02:49. The worker automatically removed needs-information/ready and set
  in-progress. Run https://github.com/moquist/rootprint/actions/runs/42440933523
  completed sandbox preparation/isolation and coordinated the sole implementation
  attempt. Durable state records exactly one attempt; no retry or reset was used.
- https://github.com/moquist/rootprint/pull/30 contains only the confirmed README
  paragraph and completion evidence in the work ledger. It uses bootstrap's existing
  maintenance process contract and post-edit acceptance with integrated/package
  checks, rather than an invented requirement delta or failing-before code test.
  README usage/setup/all-tests blocks and runtime/protocol/package bytes are intact.
- Exact head `a6be4e0cba017b76b2a3b64198a1cc2ddf2cb73d` passed Actions App `15368`
  `ci` checks `128611023725` / `128611047152` (runs `42441233582` / `42441236595`)
  and reviewer App `5631539` check `128610759974`, run
  https://github.com/moquist/rootprint/actions/runs/42441236614. API confirms owner
  `moquist` merged at 03:14:46 UTC as `f14dfc8`; issue closed one second later.
- App comment edit history verifies Next step prompts for initial active triage
  (02:58:36), clarification/readiness/automatic label cleanup (02:59:01), active
  implementation (03:02:49), linked-PR CI/review waiting (03:05:32 and 03:06:47),
  and owner Rebase and merge with no new ready label (03:08:28). Run
  https://github.com/moquist/rootprint/actions/runs/42441353262 reconciled passing
  gates before merge. Only one state comment and one human answer exist.
- Clarification task 3.2 is now evidenced (5/5 complete). OpenSpec archived the
  no-delta bug fix at `openspec/changes/archive/2026-11-07-preserve-worker-clarification-context/`
  (CLI local-date prefix); no main spec sync was needed. Documentation task 4.2
  remains open (6/7): its successful
  intake/clarification/active/check/manual-merge path is evidenced, but no hosted
  blocked-prompt example was exercised. At inspection the closed issue's worker
  state still said in-progress/merge, awaiting a later done reconciliation; this
  is not recorded as done acceptance. Local blocked/done mocks are not hosted proof.
  Do not mutate #23, bypass gates, close unrelated bootstrap/repair tasks or claim
  full autonomous maintenance/activation from this successful documentation run.
- Acceptance bookkeeping verification: credential-free
  `env -i HOME=/tmp/opencode PATH="$PWD/.venv/bin:$PATH" python3 scripts/check.py`
  passed both five-test port suites, 66 script checks, Ruff and all 10 remaining
  strict active changes after archive. Whitespace checks pass. Only this evidence,
  the verified clarification checkbox and its archive location changed; no runtime,
  README usage/test command, permission, package or protocol edit was needed.

## Completion handoff — 2026-11-08 (issue #29)

- Documentation-only completion under
  `openspec/changes/bootstrap-rootprint-ecosystem/specs/automated-maintenance/spec.md`.
  README.md adds the confirmed sentence: “`calculatedAt` is descriptive metadata
  and does not affect deterministic content identity.” It is a standalone
  paragraph after the UTC label example and before “Setup and run all tests”.
  moquist's comment #6716465117 confirmed the retained wording/placement question;
  no further clarification was needed.
- Inspected the full README diff and hash-record contract plus both ports' record
  construction. Acceptance passed: exact sentence once, exact placement, regular
  non-executable README, and removing only the inserted paragraph reproduces
  HEAD's README bytes. All usage examples and test commands remain unchanged;
  no runtime, protocol, vector or normative specification changes were made.
- Completion reran `python3 scripts/check.py`: both five-test port suites,
  66 script tests, Ruff, and all 11 strict OpenSpec changes passed.
  `python3 scripts/package_check.py` passed both installed CLI/API and package
  checks. `git diff --check` passed after this ledger update. The only changed
  files are README.md and this completion ledger; no task checkboxes or archive
  state were changed, and unrelated bootstrap/hosted acceptance remains open.
- Local verification is complete, not a claim of deployment or issue closure.
  Fresh CI and independent automated review on the latest PR revision remain
  required, followed by owner merge. No remote activation, publication, commit,
  push or merge was performed in this sandbox.

## Latest session handoff — 2026-11-08 (documentation implementation refresh)

- Owner merged diagnostic PR #27 as `544a27f`; fetched `origin/main` points there.
  Prepared `work/worker-documentation-plans-implementation-refreshed` from that
  base and replayed implementation `477d9e2`. The original local implementation
  branch remains preserved. Only the work ledger conflicted; retained both full
  diagnostic and documentation handoffs below without dropping evidence.
- All eight non-ledger implementation/artifact files are byte-identical to
  `477d9e2`. The already-merged clarification fix and provider diagnostics remain
  intact. The new PR contains only documentation intake/guidance implementation
  and this refresh evidence, rather than republishing either merged fix.
- Credential-free `env -i HOME=/tmp/opencode PATH="$PWD/.venv/bin:$PATH" python3 scripts/check.py`
  passed both five-test port suites, 66 script checks, Ruff and all 11 strict
  changes. The same environment's `python3 scripts/package_check.py` passed both
  installed CLI/API/package checks. Whitespace checks pass. Existing real sandbox/
  OpenCode verification for the byte-identical implementation is recorded below;
  this refresh did not repeat or claim a new runtime/model/provider acceptance run.
- OpenSpec remains 6/7 complete: hosted documentation/prompt acceptance stays open.
  Clarification's controlled acceptance and unrelated activation tasks also remain
  open. Primary README commands and package/protocol/dependency/workflow permissions
  are unchanged. No remote mutation, push, model request or merge occurred here.
- Next owner command from this branch: `git push -u origin HEAD`, then open a PR
  to `main` titled `feat: support worker documentation plans and issue guidance`.
  Require fresh exact-head CI and independent review, then owner manual rebase merge.
  After deployment, exercise a fresh small documentation issue and a short-answer
  clarification, inspect Next step prompts and linked PR/check/manual-merge outcomes,
  and record actual issue/run/PR evidence before marking hosted tasks complete.

## Latest session handoff — 2026-11-08 (review-provider diagnostics)

- PR #26's head `631d68d` passed all current-head CI jobs. Its original reviewer
  check `128598798741` failed with `OpenAI review request failed (HTTP 429)` and
  outcome `infrastructure`: https://github.com/moquist/rootprint/actions/runs/42437281533.
  After the owner added credits/dispatched retry, check `128600125131` approved
  the same head at 02:16 UTC: https://github.com/moquist/rootprint/actions/runs/42437710907.
  `gh pr checks 26 --required` confirmed all required checks passed; GitHub still
  showed the old Actions job red and aggregate `UNSTABLE`. There was no fresh
  reviewer failure. Owner rebase-merged #26 at 02:18 UTC as `1ab2eac`.
- Created independent `fix/review-failure-diagnostics` on fetched main and advanced
  it to the merged clarification fix. The documentation implementation is preserved
  separately at `477d9e2` on `feat/worker-documentation-plans`; refresh that branch
  against merged main before its separate publication. No agent push/merge occurred.
- This is an observability conformance fix under bootstrap's bounded/observable
  automation and the repair contract's distinguishable infrastructure diagnostics,
  preserving untrusted-input/credential isolation; no requirement delta is invented.
  Traced provider transport, check completion, CLI/hosted entrypoints, retry caching,
  worker repair consumers and workflow attribution. HTTP status reached the App
  check but the Actions exception hid it behind `blocking check recorded`.
- Permanent credential-free failing-before regression:
  `env -i HOME=/tmp/opencode PATH="$PWD/.venv/bin:$PATH" PYTHONPATH="$PWD/scripts" python3 -m unittest test_independent_review.ProviderAndIdentity.test_provider_http_failure_is_visible_in_actions_error_summary_and_check`.
  Before the fix: `FAILED (failures=1)`, `Actions failure hides the provider HTTP
  status`; captured Actions output was empty for a simulated HTTP 429. No provider
  request or GitHub write was made.
- Implemented status-only provider diagnostics in the check title/summary and at the
  shared standalone/hosted CLI boundary: an Actions error annotation and job Summary
  show HTTP status, infrastructure/input category, next action, PR/run links and a
  bounded explicit retry command for provider failures. HTTP 429 guidance explains
  quota/billing versus rate limits without inventing a subtype. HTTP 401/403, 5xx
  and other statuses have fixed configuration/service guidance. Existing outcome
  schema, failure gates, App permissions and three-attempt limit are unchanged.
- Initial tests passed but exposed Python 3.14 ResourceWarnings from unclosed HTTP
  error responses; those warnings could include the raw reason. Fixed the shared
  provider boundary to close errors without reading/logging bodies, reasons or
  headers. Tests assert closure, absence of synthetic secrets, escaped Actions
  commands, honest job-summary write failure and token revocation on CLI exit.
  Reporting runs only at the CLI boundary, so fake review failures inside ordinary
  CI tests do not create misleading annotations or replace the real job summary.
- Final credential-free focused command:
  `env -i HOME=/tmp/opencode PATH="$PWD/.venv/bin:$PATH" PYTHONPATH="$PWD/scripts" PYTHONWARNINGS=error::ResourceWarning python3 -m unittest test_independent_review test_pr_repair test_review_budget test_review_compact`
  passes 34 checks without warnings. Credential-free
  `env -i HOME=/tmp/opencode PATH="$PWD/.venv/bin:$PATH" python3 scripts/check.py`
  passes both five-test port suites, 56 script checks, Ruff and all 11 strict changes.
  `git diff --check` passes. Full diff/callers reviewed; primary README examples and
  setup/all-tests commands remain current. No package, protocol, vector, dependency,
  workflow or permission change was needed. No live model request or remote write
  occurred during diagnosis/verification.
- Locally verified reporting fix awaits owner publication, exact-head CI and
  independent review/manual rebase merge, then hosted diagnostic acceptance. Next
  owner command: `git push -u origin fix/review-failure-diagnostics`. New reports
  activate only after deployment; original runs retain their old output. #26 is
  merged, but its separate controlled clarification acceptance task remains open;
  no unrelated bootstrap/repair acceptance or activation requirement was completed.

## Latest session handoff — 2026-11-07 (documentation route implementation)

- Applying `support-worker-documentation-plans` on separate stacked branch
  `feat/worker-documentation-plans`, based on clarification fix `d4e056d`. Publish/
  merge the clarification PR first so this implementation's PR contains only its
  own changes. Both deployed acceptance tasks remain open until evidenced.
- Permanent initial documentation regression fails before routing changes:
  `env -i HOME=/tmp/opencode PATH="$PWD/.venv/bin:$PATH" PYTHONPATH="$PWD/scripts" python3 -m unittest test_issue_worker.Lifecycle.test_initial_documentation_maintenance_reaches_linked_pr`
  reports `Maintenance classification is restricted to non-code repair acceptance`
  despite an existing bootstrap maintenance contract and runnable acceptance.
  #23's observed `Plan must reference an OpenSpec contract` remains diagnosed
  evidence only: its exact unavailable model report is not inferred.
- Implemented initial/repair documentation maintenance in the shared development
  path. The coordinator supplies the main/bootstrap process contract; invalid or
  missing references/acceptance/classification remain worker-plan failures. Prose
  work uses runnable post-edit acceptance, separate phases and normal integrated/
  package checks, without fabricated requirement deltas or failing-before code tests.
- A shared final exported-diff guard checks both publication routes after completion.
  Its corpus is root/setup/package READMEs and docs Markdown/text/reStructuredText,
  regular non-executable files only. Tests cover allowed prose plus rejected late
  source/tests/configuration/workflow/policy/agent/spec and executable-mode edits.
  Existing bug regression and feature-artifact validation remain enforced.
- Every state save renders a trusted, bounded Next step separately from task text/
  clarification history. Callers select actual stage/reason; typed worker-plan/report
  and provider/runtime failures distinguish fixing the worker from resolving setup.
  Prompts cover ready, questions, remaining/exhausted budgets, active work, checks,
  repair, review retry dispatch, manual rebase merge, closed PR and done. Unknown
  failures request investigation. No model field chooses actions or grants authority.
- Durable snapshots suppress identical saves across fresh runs without losing later
  budget/recovery updates. Guidance counts against state capacity; failed comment
  access/publication does not claim a delivered prompt. Tests preserve clarification
  provenance and unchanged revision/authorization/retry/merge boundaries. Worker and
  setup guides include the documentation scope, examples and lifecycle action table.
- Final credential-free focused command
  `env -i HOME=/tmp/opencode PATH="$PWD/.venv/bin:$PATH" PYTHONPATH="$PWD/scripts" python3 -m unittest test_issue_worker test_pr_repair`
  passes 42 tests. `env -i HOME=/tmp/opencode PATH="$PWD/.venv/bin:$PATH" python3 scripts/check.py`
  passes both five-test port suites, 63 script checks, Ruff and all 11 strict changes.
  Initial integrated verification found Ruff E731 in a test helper; replaced its
  assigned lambda with a function. Final review added explicit exhausted-budget
  wording on the third failure; focused/integrated/runtime checks were repeated
  after that change and pass. Whitespace checks pass.
- Credential-free `python3 scripts/package_check.py` passed installed TypeScript/
  Python CLI/API and distribution checks. Rebuilt the real rootless Podman image,
  then `python3 scripts/worker_runtime_check.py --runtime podman` passed isolation,
  hostile artifacts, exact-head import/deletions/modes/export/mismatch checks, real
  pinned OpenCode/MCP startup and offline integrated/package checks (Node 22/Python
  3.11). Both commands used `env -i HOME="$HOME" PATH="$PWD/.venv/bin:$PATH" XDG_RUNTIME_DIR="${XDG_RUNTIME_DIR:-/run/user/$(id -u)}"`;
  image preparation preceded offline execution. No provider/GitHub credential or
  live model request was used. Full affected flows/diff reviewed; primary README
  usage/setup/all-tests examples, package/protocol/vector/dependency/permission and
  unrelated activation requirements remain current and unchanged.
- Local tasks 1.1–4.1 are complete (6/7); hosted task 4.2 remains open. Owner first
  publishes clarification branch `fix/worker-clarification-context` through fresh
  current-head CI and independent review and manual rebase merge, then publishes
  `feat/worker-documentation-plans` as its own implementation PR. After that merge,
  controlled documentation/clarification issues must evidence deployed prompts and
  linked PRs. #23 was not changed. No agent push, remote mutation, merge or activation
  occurred. Both changes stay unarchived pending their real hosted acceptance.

## Latest session handoff — 2026-11-07 (clarification-context implementation)

- Applying `preserve-worker-clarification-context` on separate branch
  `fix/worker-clarification-context`, based on merged planning head `ac9c7df`.
  Read all shared save/pause/triage/development/repair callers and bootstrap's
  existing automated-issue-lifecycle and trust/bounds requirements.
- Added runnable #23 lifecycle regression. Credential-free command:
  `env -i HOME=/tmp/opencode PATH="$PWD/.venv/bin:$PATH" PYTHONPATH="$PWD/scripts" python3 -m unittest test_issue_worker.Lifecycle.test_short_answer_retains_question_across_status_saves_and_fresh_phases`.
  Before the fix: `FAILED (failures=1)`, with `Owner reply survives, but its
  antecedent worker question is lost`; captured triage contains the owner's
  agreement but not the original question after a fresh worker/generic save.
  The first diagnostic run's assertion was hidden by coordinator error handling;
  moved the assertion outside the stub model to expose the actual missing data.
- Implemented validated, ordered clarification history in the shared durable save
  path, deduplicated by revision/question. Legacy needs-information text migrates
  with unknown original revision/cursor; erased text is never invented. Candidate
  state is checked before replacing the prior record, including in-memory history;
  publication/recovery objects keep their existing identity across status saves.
- Initial/resumed triage, plan/implement/complete and existing-PR repair receive the
  same retained questions and complete human comments with IDs/authors and question
  run/revision/cursor provenance. Removed ten-comment/4,000-character clipping;
  the existing complete-task 90,000-character guard remains at every actual phase.
  Trusted policy and operations docs describe untrusted history, legacy migration,
  the 60,000-character state limit and unchanged ready/retry/manual-merge gates.
- Credential-free focused command
  `env -i HOME=/tmp/opencode PATH="$PWD/.venv/bin:$PATH" PYTHONPATH="$PWD/scripts" python3 -m unittest test_issue_worker test_pr_repair`
  passes 32 tests, including multiple questions, duplicate saves, malformed/spoofed
  history, overflow retaining prior state, long/many replies, unanswered ambiguity,
  fresh initial/repair phases and authorization/budget/event deduplication. A test
  insertion indentation error was corrected before this successful run.
- Credential-free `env -i HOME=/tmp/opencode PATH="$PWD/.venv/bin:$PATH" python3 scripts/check.py`
  passes both five-test port suites, 53 script checks, Ruff and all 11 strict changes.
  `git diff --check` passes. Inspected the complete affected flow and diff. README
  setup/usage/all-tests commands remain current; no workflow, permission, protocol,
  package, dependency, vector, asset or unrelated activation requirements changed.
- Local tasks 1.1–3.1 are complete (4/5). Task 3.2 stays open until owner publication,
  fresh current-head CI and independent automated review, manual rebase merge and
  a new controlled short-answer issue demonstrate the deployed fix. Do not use
  #23's workaround as acceptance. No push, remote mutation or model call occurred.
  Next owner command: `git push -u origin fix/worker-clarification-context`, then
  open this fix's separate implementation PR. Keep documentation-plan implementation
  for the next change; leave this change unarchived pending hosted acceptance.

## Latest session handoff — 2026-11-07 (PR #25 conflict refresh)

- PR #25's published head is `bad80db99d6f4171b1295f683ceaf81db518719c`.
  Main advanced to `debbe91` after the clarification-context plan merged.
  Prepared `work/worker-documentation-plans-refreshed` on that base while retaining
  the original local/published planning branch. Replaying its one planning commit
  reproduced a content conflict only in `docs/local-work.md`.
- Resolved by retaining both complete planning handoffs. All five documentation/
  guidance change files are byte-identical to `bad80db`; the merged clarification
  artifacts are byte-identical to current main. This refresh remains planning only:
  neither change's implementation/acceptance tasks were marked complete.
- Credential-free `python3 scripts/check.py` passed both five-test language suites,
  47 script checks, Ruff and all 11 strict changes. Whitespace checks pass. No
  runtime, package, workflow, protocol, vector or asset files changed.
- Owner updates the existing PR branch from this refreshed branch using an
  explicit force-with-lease against the published head above. Agents do not push
  or rewrite published history. Fresh current-head CI and independent review remain
  required before manual rebase merge; no remote PR/check/settings mutation occurred.

## Latest session handoff — 2026-11-07 (clarification-context fix planned)

- PR #22 merged as `01295c9` after final head `82d439f` passed CI and independent
  review (runs `42414218342` and `42414216291`). This supersedes the earlier open-PR
  handoff. Created planning branch `docs/preserve-clarification-context` from that
  fetched main; repair hosted-acceptance tasks remain open.
- Issue https://github.com/moquist/rootprint/issues/23 exposed a clarification loop:
  the worker drops bot comments from model context, so the owner's short agreement
  loses its antecedent question. Generic triage/attempt status also overwrites the
  durable message before context construction. The owner is handling #23's immediate
  workaround; this session did not mutate the issue, labels or workflows.
- Reproduced locally without credentials/model/API access:
  `env -i HOME=/tmp/opencode PATH="$PWD/.venv/bin:$PATH" PYTHONPATH="$PWD/scripts" python3 /tmp/opencode/reproduce_clarification_context.py`.
  It fails the assertion `Owner reply survives, but its antecedent worker question
  is lost` after saving a needs-information question, adding a short human answer,
  creating a fresh worker and saving generic triage status.
- Created `openspec/changes/preserve-worker-clarification-context/`: proposal,
  design and five unchecked implementation/acceptance tasks. `skip_specs: true`
  intentionally avoids inventing requirements for a bug in bootstrap's existing
  automated issue lifecycle. The plan retains bounded clarification history in the
  existing App state, migrates recoverable legacy questions before overwrite and
  supplies complete bounded question/answer evidence to initial and repair phases.
  Ready authorization, issue-revision/attempt accounting and trust boundaries remain
  enforced; no separate chat store or new permissions are needed.
- Focused and all-change strict validation passed (10 changes); whitespace passed.
  All planning artifacts are ready, specs are explicitly skipped and 0/5 apply tasks
  are complete. No project runtime/test code changed. Next is a separate apply
  request; owner publication still requires fresh CI, independent review and manual
  rebase merge, followed by a new controlled short-answer acceptance run.

## Latest session handoff — 2026-11-07 (documentation intake and issue guidance planned)

- Created `docs/worker-documentation-plans` from fetched main `01295c9` for new
  change `support-worker-documentation-plans`. The clarification-context plan is
  preserved independently on `docs/preserve-clarification-context` at `a2869c0`;
  neither its artifacts nor issue #23 were changed by this planning task.
- #23's owner supplied explicit README wording, but the worker then reported
  `Plan must reference an OpenSpec contract` (run `42416005748`). Inspected both
  development/publication paths: `maintenance` already exists in the report schema
  but is restricted to PR repair; initial triage policy describes only bug/feature,
  and the documentation output guard is repair-only. The exact live phase report
  is unavailable, so its classification/contract value is not asserted.
- Offline reproduction with a valid existing maintenance process reference:
  `env -i HOME=/tmp/opencode PATH="$PWD/.venv/bin:$PATH" PYTHONPATH="$PWD/scripts" python3 /tmp/opencode/reproduce_documentation_plan.py`.
  It fails with `Maintenance classification is restricted to non-code repair acceptance`.
  No model/provider/GitHub call or project runtime/test edit was made.
- Plan reuses maintenance for initial docs issues, worker-selected process contracts,
  runnable acceptance rather than invented code regressions, and shared final
  documentation path/mode checks before initial and repair publication. Code,
  executable policy, configuration and normative requirement changes retain their
  proper routes. Existing verification, authorization and attempt limits remain.
- Owner also requires actionable prompts directly in GH issues. Added the
  `worker-issue-guidance` delta with state/reason-specific Next step instructions:
  answer a clarification, add `ready`, resolve setup or worker defects first, use
  an eligible retry, wait for checks, manually rebase-merge, or take no further
  action when done. `ready` triggers automatic needs-information cleanup; no
  redundant manual removal is required. Guidance is trusted/bounded/idempotent
  and separate from task questions or retained clarification history.
- Proposal, spec, design and seven unchecked tasks are ready. Focused and all-change
  strict validation pass (10 changes on this branch); whitespace passes. This is
  planning only (0/7 tasks complete). Next is a separate apply request and ordinary
  owner publication/current-head CI/independent review/manual merge, followed by
  controlled docs-intake/prompt acceptance. No push, issue update or merge occurred.

## Latest session handoff — 2026-11-07 (PR #22 independent-review fixes)

- PR https://github.com/moquist/rootprint/pull/22 is open at published head
  `b6d5440`, base `22054ac`. Its CI matrix passed, but reviewer App `5631539`
  check `128520994820` rejected two real acceptance gaps:
  https://github.com/moquist/rootprint/actions/runs/42411662221. This was a code
  rejection, not provider failure or context overflow. No retry of unchanged code
  was requested.
- Reproduced both findings before fixes with
  `python3 -m unittest discover -s scripts -p test_pr_repair.py`: the two new checks
  failed in 13 subcases (all four oversized phase requests plus nine mixed
  source/operational matrix outcomes). They reference the existing bounded-input
  and complete/actionable-diagnostic contract, not a new requirement.
- Fixed the shared `worker_agent.phase` boundary: serialize final task data once,
  enforce the shared 90,000-character ceiling before any OpenCode launch, and send
  exactly that checked serialization. Reports added by triage/planning and final
  verification count on every actual request, including initial-issue phases.
  Exact-limit tasks remain accepted; overflow is rejected without truncation or
  subprocess invocation.
- Fixed CI classification to inspect all non-aggregate matrix jobs before selecting
  failed source-verification jobs. Operational, unfinished and unsupported outcomes
  now block mixed-failure repair, including timeouts/cancellation alongside a source
  failure. Failed-job steps are likewise checked before filtering; normal successful
  sibling jobs and successful/skipped cleanup steps still permit actionable repair.
- Credential-free `python3 scripts/check.py` passed both five-test port suites,
  47 script checks, Ruff and all nine strict changes. The focused repair suite now
  has 15 passing checks, including exact context boundaries, report-driven growth,
  mixed job/step outcomes and positive controls. Workflow, sandbox execution
  boundary, package/protocol/vector bytes and README test commands are unchanged.
- Repairs are appended locally on the same `feat/worker-pr-repair` branch. Owner
  next runs `git push origin feat/worker-pr-repair` to update PR #22; new-head CI and
  independent review are required before manual rebase merge. No agent push, check
  retry, remote settings mutation or merge occurred. Hosted acceptance tasks 5.2–5.3
  remain open; local fixes do not claim reviewer approval or deployment acceptance.

## Latest session handoff — 2026-11-07 (existing worker PR repairs implemented locally)

- Owner merged the planning PR; implementation branch `feat/worker-pr-repair`
  starts at fetched main `22054ac`. Applied `repair-worker-pull-requests` locally:
  initial `ready` authorization and the same three-attempt budget now cover repairs
  on the existing worker PR/branch. Legacy PRs require explicit authorization;
  changed scope, drafts/closure/foreign identity and exhaustion pause or stop work.
- Added bounded expected-App gate/diagnostic collection with the workflow's
  read-only token (explicit contents/issues/PR/checks/Actions reads), and typed
  reviewer output distinguishing validated findings from infrastructure failures.
  CI input is failed verification-step metadata plus complete check annotations
  for the matching run attempt. Setup/runner/dependency failures are operational
  blockers. No arbitrary log URL/command or PR artifact executes on the host.
- Exact immutable head source is imported only inside the offline sandbox and
  verified against its complete tree, including deletions/modes. Ambient OpenCode
  files remain inert source; host/model config stays fixed. Repairs reuse the
  shared plan/implement/complete path, failing-before/passing-after bug regression
  and final integrated/package verification. Non-code maintenance requires runnable
  acceptance and cannot change executable/configuration source.
- Publication creates a non-force child commit on the same branch after freshness
  checks. Durable commit intent, candidate and publication state recover lost
  commit/ref/state responses without duplicate PRs or model work. A runnable test
  initially exposed pending publication being erased on a failed final state save;
  reloading durable state before recording failure fixed the shared recovery path.
  Intervening owner work is preserved. Fresh required checks precede a ready-for-
  owner-merge status; no merge, auto-merge, self-approval or settings writes exist.
- Verification passed: credential-free `python3 scripts/check.py` (both five-test
  port suites, 45 script checks, Ruff and nine strict changes), focused 13 repair
  checks, `python3 scripts/package_check.py`, Actionlint 1.7.7 on all three workflows,
  and whitespace checks. Real rootless Podman image build and
  `python3 scripts/worker_runtime_check.py --runtime podman` passed isolation,
  hostile artifact rejection, exact-head import/deletion/executable-mode/export
  baseline/mismatch checks, pinned OpenCode 1.19.4 config, real MCP startup and
  offline integrated/package checks (Node 22/Python 3.11). Latest added pagination,
  size and no-change scenarios also pass host checks. No live model or App write
  was made. Full affected flows/diff were inspected; protocol, packages, vectors,
  dependencies and README usage/setup/all-tests commands are unchanged.
- Local implementation/verification tasks 1.1–5.1 are complete (10/12). Hosted
  tasks 5.2–5.3 remain open: owner publishes through exact-head CI and independent
  review, manually rebase-merges, then controlled real CI/reviewer-failure repairs,
  new-head checks, retry/recovery/hostile/stale-head acceptance and manual merge
  outcome must be evidenced. Bootstrap remains 17/27 and changes stay unarchived.
  Agents do not push or enable auto-merge. Documentation and activation output
  explicitly describe repair as local implementation pending hosted acceptance.
- Verified implementation commit: `194ef79` on `feat/worker-pr-repair`. Deployed
  reviewer/hosted-entrypoint source replay accepts it at 912,106 text bytes with
  287,894 bytes remaining, using merged planning PR #21's full discussion as proxy
  plus 8,192 bytes extra allowance. Command:
  `python3 /tmp/opencode/replay_review_refresh.py 21 HEAD`. This is immutable-source
  sizing, not independent model approval or the new PR's actual discussion.
  Owner next pushes this branch and opens its implementation PR to main; require
  fresh exact-head `ci` and `independent-review`, then manual rebase merge before
  hosted repair acceptance. Final evidence commit is sized separately.

## Latest session handoff — 2026-11-07 (repair planning PR prepared)

- Owner merged activation PR https://github.com/moquist/rootprint/pull/20;
  fetched main is `99e4e6a431ad6c196034dbf1520362c5e0dfe581`. Its exact original
  head `a342086` passed CI run `42402310045` and independent-review run
  `42402310052`. Created `docs/worker-pr-repair-plan` from that merged base and
  cherry-picked only planning commit `e62f668` as `052c4e8`; preserved the old
  published branch/history. The PR diff is the five change files plus this ledger.
- Reverification passed: credential-free `python3 scripts/check.py` (both five-test
  port suites, 32 script checks, Ruff, nine strict changes), focused strict repair
  change validation and whitespace checks. All 12 implementation tasks stay open.
- Deployed-reviewer sizing replay accepted planning snapshot `052c4e8`: 671,985
  text bytes, 528,015 below the hosted limit, using PR #20's discussion as a proxy
  plus 8,192 bytes headroom. This is a source/context budget check, not review of
  a newly created PR or model approval. Replay script:
  `/tmp/opencode/replay_review_refresh.py 20 HEAD`; final handoff commit is sized
  separately. No model request or PR source execution occurred.
- PR title: `docs: plan bounded worker PR repairs with manual merging`.
  Prepared body: `/tmp/opencode/worker-pr-repair-plan-pr.md`. Owner publishes with
  `git push -u origin docs/worker-pr-repair-plan`, then opens a PR to `main` using
  that title/body. Wait for fresh `ci` and `independent-review`, then manually
  rebase-merge before requesting the separate apply phase. No agent push, PR
  creation, implementation, remote setting change or merge occurred.

## Latest session handoff — 2026-11-07 (bounded PR repair planning)

- Owner approved specifying automatic repairs to existing worker PRs while keeping
  final PR approval as the owner's manual rebase merge. Created
  `openspec/changes/repair-worker-pull-requests/`: proposal, additive
  `pull-request-repair` delta, design and 12 unchecked implementation/acceptance
  tasks. This session is planning only; no worker behavior or deployment changed.
- Initial `ready` covers bounded repairs of the authorized issue revision on the
  same PR/branch. Initial implementation and repairs share three attempts; worker
  commits/events do not reset them. Legacy PRs require explicit repair authorization.
  The plan requires current-head expected-App evidence, typed reviewer outcomes,
  exact-head credential-free execution, separate phases and regression evidence,
  non-force append-only publication, durable lost-response recovery and fresh
  CI/review before reporting ready for owner merge. Infrastructure failures,
  ambiguity, scope changes and exhaustion stop or pause work with concrete status.
- Inspected worker early returns, durable revision/retry/publication flows, sandbox
  seeding/export, agent phases/policy, reviewer check output, workflow triggers and
  existing tests. Main specs remain empty; bootstrap's maintenance delta is the
  baseline. Its later automatic-merge requirement is retained, not activated or
  completed by this manual-merge repair capability. Bootstrap remains 17/27.
- Next: a separately requested apply phase for `repair-worker-pull-requests`.
  Keep hosted acceptance tasks open until owner deployment and real controlled
  run evidence, including failure/repair/fresh checks, a passing PR left open for
  owner merge, exhausted attempts and stale-head/recovery scenarios. No push,
  remote settings change, merge or publication occurred. Preserve archive/baseline
  prerequisites and existing App-bound no-bypass gates.
- Planning verification passed: focused strict validation, then credential-free
  `python3 scripts/check.py` (both five-test port suites, 32 script checks, Ruff
  and all nine strict changes), plus `git diff --check`. OpenSpec reports all
  four planning artifacts ready; 0/12 implementation/acceptance tasks are done.

## Latest session handoff — 2026-11-07 (activation report correction)

- Fixed the obsolete activation report under bootstrap's existing accurate setup
  status requirement; no new behavior contract or activation authorization was
  needed. `scripts/activation.py` now separates dated, repository-specific
  `recordedHostedEvidence` from remaining blockers and explicitly reports
  `liveRemoteChecksPerformed=false`. Evidence links cover CI, reviewer approval,
  merge rules and issue #12's manual lifecycle. They remain historical even if
  this checkout has no origin or points elsewhere. Origin URLs and credentials
  are not exposed; no GitHub/provider request is made.
- `githubMaintenanceActive` and `publishingActive` remain false, and
  `--require-active` still exits 1. Remaining requirements name hostile-input,
  repeated-event, retry/recovery and failure-deduplication acceptance, controlled
  bug/regression work, auto-merge, and release/registry setup. Recorded evidence
  does not assert current settings, permissions, provider access or runner health.
- Added a runnable regression in `scripts/test_activation.py`; before the fix,
  credential-free activation tests failed with missing `liveRemoteChecksPerformed`.
  After the fix all three pass, covering historical evidence with/without origin,
  only a local Git lookup, secret-URL redaction and fail-closed `--require-active`
  even with synthetic provider/write environment values. Updated README,
  automation/setup and verification guidance that repeated obsolete claims.
- Bootstrap task 6.3 stays open: this corrects reporting but does not implement a
  live audit of every installation, permission and missing-configuration case.
  Bootstrap remains 17/27; the next acceptance work is still controlled worker
  bug/regression and adversarial/recovery scenarios. No remote activation, push,
  merge or publication is authorized by this fix.
- Verification passed with an empty credential environment: focused activation
  tests (3), `python3 scripts/check.py` (both five-test port suites, 32 script
  checks, Ruff and eight strict changes), and `git diff --check`. The actual JSON
  command emitted the dated evidence and remaining blockers with both active
  flags false. README usage/setup/all-tests commands are unchanged.

## Latest session handoff — 2026-11-07 (bootstrap hosted evidence reconciliation)

- Owner rebase-merged PR https://github.com/moquist/rootprint/pull/14 at
  `2026-11-07T03:03:39Z`; fetched main is
  `09534603aa76640ee8e23abd567e6e35301a90bd`. Issue #12 is closed. Its App-authored
  [state comment](https://github.com/moquist/rootprint/issues/12#issuecomment-6688011714)
  records `done` and the merged PR, confirmed by successful worker reconciliation
  https://github.com/moquist/rootprint/actions/runs/42332113682. Earlier handoffs'
  PR #14 publication/merge blockers are resolved.
- Bootstrap task 4.1 is complete: exact published head
  `13ed25479d6c9abeaf61bee136fad4518bf22182` passed all four matrix jobs (Linux,
  macOS, Windows with Node 22/Python 3.11; Linux with Node 24/Python 3.14) and `ci`:
  https://github.com/moquist/rootprint/actions/runs/42332002332. Inspected read-only
  CI workflow runs both ports, integration, builds/static checks, strict specs and
  packaged checks. Actions App `15368` check `128280773328` belongs to that head.
- Bootstrap task 6.1 is complete: re-fetched App `5631539` checks `127743430168`
  (old-head success), `127744827545` (new-head failure), and `127746465847`
  (fresh new-head success). Historical pending/failure merge-blocking observations
  are preserved in `docs/png-review-acceptance-evidence.json`; only their generic
  freshness/gate evidence applies, not superseded image-content requirements.
  Current image-excluding reviewer also approved PR #14's exact published head:
  check `128280455200`, https://github.com/moquist/rootprint/actions/runs/42332000613.
  Inspected workflow executes trusted default-branch orchestration, not PR code.
- Re-read ruleset `26673301`: active, no bypass actors, strict App-bound `ci` and
  `independent-review`, zero required human approvals, rebase-only and linear
  history. Repository permits rebase only; `allow_auto_merge=false` remains true.
  Bootstrap is now 17/27 complete; no automatic merge or publication is claimed.
- Task 5.4 remains open: original worker run
  https://github.com/moquist/rootprint/actions/runs/42243993367 passed its hosted
  sandbox preflight and separate plan/implement/complete phases (artifacts retained
  in `f3e17ed:docs/local-work.md`), but this documentation request had no failing
  bug regression. The owner refreshed its branch before merge. This is evidence
  of the manual-merge path, not all bootstrap acceptance scenarios.
- Next local fix: `scripts/activation.py` hard-codes obsolete claims that hosted
  CI, App/provider use and reviewer gates are unverified. Reproduce that inaccurate
  status with a runnable check, then make the report distinguish recorded hosted
  evidence from remaining activation requirements without treating recorded
  evidence as a live health probe. Task 6.3 stays open until verified. Remaining
  hosted checks include controlled bug/regression work, hostile input, repeated
  events, exhausted attempts/recovery, and failure deduplication (tasks 5.2–5.5).
  Auto-merge and release automation remain separate activation work.
- Verification: credential-free `python3 scripts/check.py` passed both five-test
  port suites, 31 script checks, Ruff and all eight strict changes. Actionlint
  1.7.7 passed all three workflows. SSH fetch failed (missing usable public-key
  authentication); public HTTPS fetch succeeded without changing remotes or
  accessing credentials. Branch `docs/bootstrap-hosted-acceptance` starts from
  fetched main. Agents do not push; owner publication still uses current-head CI
  and independent review. Bootstrap and dependent deltas remain unarchived.

## Latest session handoff — 2026-11-06 (README CLI PR refresh)

- Owner merged image-exclusion PR https://github.com/moquist/rootprint/pull/18;
  current fetched base is `2140a18`. Exact original head `819e542` passed CI
  https://github.com/moquist/rootprint/actions/runs/42316231446 and reviewer App
  `5631539` approval https://github.com/moquist/rootprint/actions/runs/42316229805.
  Hosted 1,200,000-byte text budget and image exclusion are now deployed.
- Refreshing README/CLI PR https://github.com/moquist/rootprint/pull/14 on a
  separate `work/readme-cli-refreshed` branch. Original published head and full
  worker planning/implementation/completion evidence are preserved on
  `backup/readme-cli-original` at `f3e17ed:docs/local-work.md`. The worker had
  verified both exact stdin/API demos, integrated/package checks and strict specs;
  the current refresh re-verifies those results before handoff.
- Resolved the ledger conflict by retaining current main and this concise record,
  rather than restoring superseded historical handoffs (including obsolete squash
  and visual-review instructions). README change remains CLI-first documentation
  only. Current-head checks and owner merge remain required; issue #12 is not
  complete until merged. No agent push or published-history update occurred.
- Refresh verification passed on Linux: both exact README stdin pipelines emit
  `rootprint-v1`/`sha256`, full digest
  `d331f806a7ada5308a00a03f350fd885f492ee54ea4d621af24ef45ba9b88559`, live UTC
  metadata and the matching 24-character label suffix. Both exact secondary API
  blocks pass their assertions and emit the documented fixed-clock digest/label.
  Setup/all-tests text is byte-identical to current main; CLI demos precede APIs.
- Credential-free `PATH="$PWD/.venv/bin:$PATH" python3 scripts/check.py` passes
  both ports, 31 script checks, Ruff and all eight strict changes.
  `python3 scripts/package_check.py` builds/installs both distributions and passes
  their real CLI/error/API checks; `git diff --check` passes. No runtime, dependency,
  protocol, vector or asset bytes changed. Check script:
  `/tmp/opencode/check_readme_usage.py` (executes the four README blocks verbatim).
- Deployed main coordinator/hosted entrypoint replay of snapshot `146e25b` on
  `2140a18` uses complete actual PR #14/issue #12 discussions plus another
  8,192-byte discussion allowance: 622,437 text bytes, leaving 577,563 below the
  1,200,000-byte ceiling. Metadata digest:
  `af1997ab975815b32955cc4cbcb5047530d360cff1614c85667a7e71ba6fdf48`.
  Replay: `/tmp/opencode/replay_review_refresh.py 14`; no model request or PR source
  execution. Final evidence commit is measured again before handoff.
- Budget bridge task 1.3 is now evidenced by owner deployment and merged PR #18's
  exact-head CI/App approval above. PR #14 still needs owner publication, fresh
  checks and rebase merge; its original remote branch/head remains unchanged.

## Latest session handoff — 2026-11-06 (PR #18 refresh verified locally)

- Owner rebase-merged budget PR https://github.com/moquist/rootprint/pull/19;
  fetched trusted main is `3765527b14e0643664d927fd10f1ed91ee5a70ac`.
  CI: https://github.com/moquist/rootprint/actions/runs/42314589222.
  Reviewer App `5631539` approved original exact PR head
  `be5544cd8bb69143a927a33f00163c206e2484bd`:
  https://github.com/moquist/rootprint/actions/runs/42314589003.
- PR #18's published head remains `afc0ccd0a5546fa7db7c69cb2ebd33018ddd9c23`.
  Prepared a separate local `work/exclude-image-review-refreshed` branch on the
  merged budget base; image-exclusion replay commit is `cf0d679`. Original local
  and remote `feat/exclude-image-review` were preserved. The only rebase conflict
  was reviewer documentation: retain 1,200,000 hosted/600,000 standalone text
  budgets and remove all image-content budgets/validation requirements.
- Credential-free integrated checks pass both ports, 31 script checks, Ruff and
  all seven strict changes; whitespace passes. The deployed trusted coordinator
  and actual hosted entrypoint accept the exact refreshed snapshot at 702,989
  bytes including 8,192-byte discussion allowance, leaving 497,011 bytes.
  Replay uses immutable Git data and no model request/PR-code execution:
  `/tmp/opencode/replay_refreshed_pr18.py`. A later documentation-only evidence
  commit is measured separately before handoff.
- Updating existing PR #18 to this rebased history requires owner authorization
  for a force-with-lease update; agents still do not push. No published branch,
  PR, check, settings, or required gate was mutated. Fresh current-head CI and
  reviewer App acceptance remain required after owner publication; budget task
  1.3 remains open until those hosted results exist.

## Current handoff — 2026-11-06

- Owner approved `exclude-images-from-review`: remove PNG parsing, visual input,
  image budgets and visual acceptance gates. Common image assets (including SVG)
  are excluded without fetching bytes; paths/modes remain visible and README text
  is reviewed. The README logo stays. This supersedes PNG requirements and the
  compact-JSON delta's image-label clauses. Historical PNG evidence below is not
  an ongoing requirement. Local implementation is verified; no deployment of
  image exclusion is claimed. Owner pushes through ordinary current-head CI and
  independent review; no agent push or remote setting change was made.
- Image-exclusion verification: 14 focused reviewer checks passed;
  `PATH="$PWD/.venv/bin:$PATH" python3 scripts/check.py` passed 5 TypeScript tests,
  5 Python tests, 30 script checks (including integration), Ruff, and strict
  validation of all six active changes. Initial strict validation rejected a long
  requirement and prose above the first spec section; both were corrected before
  the passing integrated run. `git diff --check` passed. Bootstrap synchronization
  remains prerequisite to archiving dependent changes; hosted acceptance is not
  inferred from local checks.

- Owner authorized compacting superseded handoffs to unblock review-context
  deployment. Full original ledger: `5444d19:docs/local-work.md`; older PNG
  implementation evidence: `6ee87b7:docs/local-work.md`. Both are preserved Git
  history, not extra head files that would consume review context again.
- Preparing three sequential local branches: `docs/compact-review-ledger`,
  `test/review-context-compat`, then `feat/review-context-dedup`. Owner pushes and
  rebase-merges each through current-head CI and independent App review before
  the next stage is refreshed. Agents do not push. No gate may be bypassed.
- PR #14 (`f3e17ed313b0fc07dc4de59509db2c7345fcdfc6`, base
  `5444d196da416c3e9fd06505375f3d5ed67d7eef`) is blocked by the existing
  600,000-byte reviewer limit: measured text context 645,622 bytes, including
  101,095 bytes of contracts duplicated from head source. New pooling behavior
  is planned in `openspec/changes/deduplicate-review-context/` on the implementation
  branch. Preparation branches deliberately exclude that additive plan.
- Task/evidence completion and deployment status must reflect actual checks.
  Offline sizing is not model approval. Preserve discussions, immutable sources,
  all existing limits, reviewer identity, freshness, and credential isolation.

## Requirements and current state

- AI authors code, tests, and maintenance; humans supply requirements and account
  authorization. Follow `AGENTS.md` and OpenSpec: inspect complete affected flows,
  reproduce bugs before fixing shared causes, propose behavioral changes before
  applying, verify tasks before checking them off, and commit verified local work.
  Standing owner authorization covers local commits, not pushes or publication.
- TypeScript and Python libraries/CLIs and shared vectors are locally verified.
  Rust follows conformance in a separate change. Preserve published `rootprint-v1`
  bytes. Pre-publication rename was expressly authorized, including protocol tag;
  `fad5bd5` records rename/labels and verification. UTC labels are metadata, not
  content identity. License is EPL-2.0 with package source/license checks.
- Primary README must permanently include simple usage for every port and
  copy/paste setup plus all-tests commands, cross-language and packaged CLI checks.
  Synchronization is only a proposal in `docs/synchronization.md`: persistent tree
  storage needs a separate change before sync implementation.
- Bootstrap is unarchived with incomplete hosted lifecycle/activation, automatic
  merging, and release tasks. Do not archive it or claim autonomous maintenance
  complete. Rename and label changes have 6/6 tasks complete. Synchronize bootstrap
  before archiving dependent deltas. PNG acceptance is recorded in its tasks and
  `docs/png-review-acceptance-evidence.json`, added by `24c18d8`.
- Worker implementation `d00496b` uses credential-free, offline containers and
  isolated OpenCode/MCP, durable attempt accounting, bounded retries and recovery,
  App-scoped writes, and manual merging. Reviewer implementation `2c28616` is
  stateless/tool-free, fetches immutable blobs without executing PR code, enforces
  complete structured assessments, exact-head/base/task freshness, App attribution,
  cache invalidation and fail-closed input limits. PNG support is now deployed.
- Worker build fix `5444d19` makes Docker archive recognition explicit. PR #14 is
  the worker's README/CLI demonstration change for issue #12; its independent
  review is blocked on context size. No refreshed approval is claimed.

## Hosted evidence and effective policy

- Owner rebase-merged PNG plan/implementation and logo/acceptance PRs. Preserve
  `backup/readme-logo-original` (`c6f7adc`) and original PNG blob
  `68e55fbadc2a7711906c2b1022b43b3fd691ec29` (425,335 bytes, 1005×419).
- PR #9 trusted PNG implementation base `47f6888`: exact-head reviewer App approval
  https://github.com/moquist/rootprint/actions/runs/42171867112 and CI
  https://github.com/moquist/rootprint/actions/runs/42171867042.
- PR #10 logo head `6dba341`: App approval explicitly inspected motif/wordmark,
  https://github.com/moquist/rootprint/actions/runs/42172497614; CI
  https://github.com/moquist/rootprint/actions/runs/42172498444. Later fresh-head
  and intentional failure-blocking acceptance, check IDs and API captures are in
  `docs/png-review-acceptance-evidence.json` and commits `f8f4bbe`, `114b775`,
  `26111e5`, `24c18d8`. These supersede older pending PNG acceptance handoffs.
- Inspected ruleset `Rootprint default branch` ID `26673301`:
  https://github.com/moquist/rootprint/rules/26673301. Active/no bypass actors,
  required PR with resolved threads, no routine human approval, strict current-base
  `ci` from Actions App `15368` and `independent-review` from App `5631539`, deletion
  and force-push protection, rebase-only linear history. Repository rebase enabled;
  squash/merge commits and automatic merging disabled. Earlier squash instructions
  were superseded by explicit owner rebase-only authorization.
- `INDEPENDENT_REVIEW_ENABLED=true` and reviewer App ID `5631539` were verified;
  actual PNG review/check attribution and merge blocking have hosted acceptance.
  Do not generalize those results to unfinished bootstrap issue lifecycle,
  auto-merge, publishing, or this deduplication deployment. Keep auto-merge off.
- GitHub CLI/keyring authentication works; prefer `gh`. Fallback:
  `nix --extra-experimental-features 'nix-command flakes' run nixpkgs#gh -- ...`.
  Never print/retrieve tokens. Historical SSH/auth failures are not current proof
  of an access blocker or permission to obtain push credentials. Owner permission
  to manage GitHub settings does not authorize pushing, merging, or publishing.

## Local verification and resolved failures

- README setup followed by `python3 scripts/check.py` runs both port suites,
  shared integration, script acceptance checks, Ruff, and strict OpenSpec checks.
  Last PNG implementation run passed both ports and 29 script checks (14 reviewer)
  with `PATH="$PWD/.venv/bin:$PATH" python3 scripts/check.py`; whitespace passed.
- `python3 scripts/package_check.py` builds and installs both packages in temporary
  environments and checks installed CLI/error/API examples and EPL source/license
  contents. `scripts/vector_reference.py --check` verifies all 28 SHA-256 vectors
  with OpenSSL plus sum8. `scripts/clean_check.py --mutations` checks source-only
  setup/integration/packages and detects canonical/order/prefix regressions.
- Integration covers 80 deterministic nested inputs and fixed clocks under UTC,
  Los Angeles and Tokyo. Local evidence includes Node 22.23.4/24.22.2 and Python
  3.14.3 on Linux; do not invent Windows/macOS or other runtime results.
- Actionlint 1.7.7 passed CI/worker/reviewer workflows. Rootless Podman worker
  runtime checks passed real offline isolation, hostile symlink rejection,
  OpenCode 1.19.4 permissions, MCP startup, model catalog and packaged CLI checks
  on Node 22/Python 3.11; no model request or GitHub write was made by local checks.
- Resolved failures: complete ISO dates avoid JS year-zero misparse; renamed
  editable Python package reinstalled; old empty OpenSpec dirs removed; Podman
  tmpfs/safe.directory adapted; offline npm metadata warmed; streamed output avoids
  inherited file-size restriction; exact ANSI-stripped MCP connection status avoids
  matching "disconnected". Reviewer fake App fixture needed repository identity.
- PNG context overflow (654,915 combined; 649,729 after plan) required owner-approved
  staged PRs and ledger compaction; planning snapshot fit at 576,664. That was a
  deployment workaround, not authorization to raise limits or omit source. Full
  split evidence/commits remain in the historical ledger. No unresolved local
  implementation failure was recorded in that handoff.

## Remaining activation

- Finish the staged deduplication change and exact PR #14 source/discussion replay,
  then owner deployment and real current-head CI/reviewer acceptance. Keep hosted
  tasks open while evidence or deployment is missing.
- Bootstrap tasks remain the authority for controlled issue-to-PR lifecycle,
  durable hosted recovery/concurrency/retry acceptance, automatic merge activation,
  publishing account ownership, release identity and end-to-end issue-to-merge
  evidence. Real provider access/App operations must be evidenced, not inferred
  from local fake transports or the existence of an origin remote.
- Setup references: `docs/issue-worker.md`, `docs/independent-review.md`,
  `github-automation-setup-instructions.md`, and active OpenSpec tasks. No scheduled
  local agent daemon is running. No publication is authorized by this ledger.
