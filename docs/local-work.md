# Local work ledger

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
