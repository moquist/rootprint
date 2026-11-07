# Local work ledger

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
