# Local work ledger

## Latest session handoff — 2026-11-06

### Owner instructions and immediate next action

- The owner asked to save state and stop so a new session can resume.
- **Do not push.** The owner explicitly performs all pushes. Local verified
  commits remain authorized. This instruction is also recorded in `AGENTS.md`.
- The owner subsequently authorized the agent to execute the previously supplied
  `gh` branch-protection/settings commands. That authorization is for GitHub
  settings, not pushing, merging, publishing, or enabling automatic merges.
- Next: inspect the repository and existing rules through `gh`, apply the
  approved manual-merge settings/ruleset, and verify the effective rules. No
  remote mutation has been executed yet. The first `gh repo view` was aborted
  when the owner requested this handoff; repository identity, current remote
  state, and existing protections have not been inspected.

### Authentication and tooling

- GitHub authentication now works: `gh auth status` through Nix reported the
  active `moquist` account using the keyring. Do not print or retrieve tokens.
- `gh` is now on `PATH` at the global Devbox profile. Prefer plain `gh` commands.
  If needed, the verified fallback invocation is
  `nix --extra-experimental-features 'nix-command flakes' run nixpkgs#gh -- ...`.
- Earlier SSH fetch/public-key failure is historical, not a reason to request
  push credentials: the owner handles pushes. No fetch or push is needed to
  configure GitHub branch rules.

### Branches and commits

- Current branch: `feat/png-review`; planning commit `24b0acd` based on local
  `main` at `2c28616`. This handoff adds only local maintenance documentation.
- `2c28616`: independent reviewer implementation (tool-free OpenAI review).
- `d00496b`: isolated OpenCode issue worker implementation (manual merging).
- `docs/readme-logo` at `c6f7adc`: owner's unchanged `rootprint-horizontal.png`,
  README image/alt text, name semantics (Merkle root + fingerprint, pun on
  footprint), and PR-preparation evidence. Preserve this branch and asset.
- The PNG is 425,335 bytes, 1005 by 419 pixels. It is on the logo branch, not the
  current support branch. The existing reviewer rejects it under its text-only
  100,000-byte file limit. No logo PR has been created.
- Local `main` tracks `origin/main` at `2c28616`; this is local tracking state,
  not a newly verified remote head. The owner reported pushing and passing CI.

### Approved GitHub configuration to apply

- Discover repository/default branch with `gh repo view`/`gh api`. Inspect
  existing repository/organization rulesets and branch protections first.
- Resolve CI's actual GitHub Actions App ID from the default branch's `ci` check
  (`/commits/{ref}/check-runs?check_name=ci&filter=latest`). Read the public numeric
  reviewer App ID from Actions variable `REVIEWER_APP_ID`; do not read PEM keys.
- Create/update the named repository ruleset **Rootprint default branch**,
  target `branch`, enforcement `active`, `bypass_actors: []`, and ref condition
  `include: ["~DEFAULT_BRANCH"]`, `exclude: []`.
- Rules: `deletion`, `non_fast_forward`, and `pull_request` with
  `allowed_merge_methods: ["squash"]`, `dismiss_stale_reviews_on_push: true`,
  `require_code_owner_review: false`, `require_last_push_approval: false`,
  `required_approving_review_count: 0`, and
  `required_review_thread_resolution: true`.
- Require `ci` restricted to the discovered Actions App and `independent-review`
  restricted to the reviewer App, via `required_status_checks` entries with
  numeric `integration_id`; set `strict_required_status_checks_policy: true`.
- Repository settings: `allow_auto_merge=false`, `allow_squash_merge=true`.
  Preserve unrelated protections; detect conflicting/duplicate named rulesets.
  Missing IDs, insufficient permissions, or unsupported private-repo plan
  enforcement must become explicit blockers, never weakened gates.
- Verify the resulting ruleset, repository merge settings, and effective rules
  using `/repos/{owner}/{repo}/rules/branches/{branch}`. Only claim what the API
  actually verifies; end-to-end review/merge acceptance remains separate.
- These fields were checked against GitHub's REST ruleset documentation, and the
  supplied Bash command block was syntax-checked. It has not been executed live.

### PNG support: planning complete, implementation not started

- Change: `openspec/changes/review-png-assets/`; four planning artifacts plus
  `.openspec.yaml` committed in `24b0acd`. All four active OpenSpec changes pass
  `openspec validate --all --strict`; `git diff --check` passed.
- The propose skill required stopping at the planning/apply boundary. There are
  **0/7 PNG tasks complete**. Resume implementation only in the separate apply
  workflow after an apply request, e.g. `/opsx-apply review-png-assets`.
- Design: static PNGs as labeled inline Responses API `input_image` data, linked
  to exact Git blob SHA, path, and head/baseline role. Include before/after image
  versions and support image findings at line zero. No local raster decoding,
  PR execution, external image URLs, tools, or credential exposure.
- Limits: 1 MiB per version, four versions/2 MiB total decoded bytes, dimensions
  at most 4096 per side and 8,000,000 pixels. Keep text limits unchanged. Validate
  signature/IHDR/chunk framing/CRCs/IEND and reject animation/malformed PNGs.
- Reuse `scripts/independent_review.py`, existing reviewer tests, and trusted
  policy. Add no dependency; keep exact-head/freshness/App/credential guards.
- After the owner deploys PNG support, refresh the logo branch against that
  base and use it for the controlled approval-path PR. Keep actual hosted
  acceptance tasks open until PR/check/run evidence is recorded.

### Verification baseline and remaining activation

- Latest implementation verification: `.venv/bin/python scripts/check.py` passed
  both language suites, all 24 script checks, static checks, and strict specs.
  Actionlint 1.7.7 passed CI, worker, and reviewer workflows. No runtime code
  changed during PNG planning or this handoff.
- Bootstrap remains 15/27 verified tasks complete; do not archive it. Its
  automated-maintenance delta is the current baseline; the PNG additive delta
  depends on synchronizing/archiving bootstrap first.
- App installations/permissions, actual OpenAI API access, enabled variables,
  independent check attribution, current-head invalidation, and enforced merge
  blocking still need hosted inspection/acceptance. Do not describe them as
  running or verified merely because authentication or CI works.
- References: `docs/independent-review.md`, `docs/issue-worker.md`,
  `github-automation-setup-instructions.md`, and the PNG change artifacts.

## Bootstrap

- Contract: `openspec/changes/bootstrap-rootprint-ecosystem/`.
- Status: both local libraries/CLIs are implemented and verified; bootstrap
  remains open because remote automation is not implemented/activated/verified.
- Decision: TypeScript and Python first; Rust is a separate follow-up change
  after shared conformance succeeds.
- Decision: work locally until the owner pushes to GitHub. Prepare remote
  gates without claiming they have run.
- Evidence: task checkboxes record only completed verification; external
  activation remains unchecked.
- Git: initialized locally on `main` at the owner's request. Initial history
  separates the OpenSpec/agent foundation, both language implementations and
  conformance checks, and CI/activation preparation. No remote is configured.
- License: the owner selected Eclipse Public License 2.0 (`EPL-2.0`). Root and
  package license copies are included; distribution checks verify license
  metadata, identical license text, and included sources.

## Remote activation debt

Until pushed, there is no GitHub issue ledger, unattended event-driven worker,
hosted Windows/macOS validation, independent PR review, or enforced merge gate.
The local ledger and Linux checks cover development evidence, not those services.
No scheduled local agent daemon is running.

Before activating: choose repository visibility, install a scoped
GitHub App, configure model access and an isolated worker, configure required
checks with no bypass, and verify a controlled issue-to-merge run. Registry
ownership and publishing identity are separate release prerequisites.

## Verification evidence

- `npm run check`: TypeScript builds and passes committed preimage/digest,
  native-input, custom-provider, and UTC-label checks.
- `.venv/bin/python scripts/check.py`: Python tests, cross-language integration,
  static checks, and strict OpenSpec validation pass on this Linux host.
- `.venv/bin/python scripts/package_check.py`: both distributions build, install
  into temporary environments, and pass CLI/error/API example checks.
- `.venv/bin/python scripts/vector_reference.py --check`: all 28 committed
  SHA-256 preimages/digests independently agree with OpenSSL.
- `.venv/bin/python scripts/clean_check.py --mutations`: source-only reproduction
  passes; intentional changes to canonical bytes, array ordering, and prefix
  length fail their expected tests in disposable copies.
- `go run github.com/rhysd/actionlint/cmd/actionlint@v1.7.7 .github/workflows/ci.yml`:
  prepared CI workflow passes syntax/expression checking. This is not a hosted run.
- Cross-language integration includes 80 deterministic generated nested inputs
  and checks fixed-clock records under UTC, Los Angeles, and Tokyo environments.
- Node 22.23.4 passes the integrated checker on this Linux host; Node 24.22.2
  passes the TypeScript suite. Python verification used 3.14.3; Python 3.11 and
  non-Linux runtime evidence remain pending hosted CI.
- Built distributions also pass through their installed `rootprint` console
  entry points (not only direct module execution).

## Failures and resolutions

- Initial year-zero test used JavaScript's permissive `0000-01-01Z` parsing,
  which means year 2000 rather than year zero. A diagnostic confirmed this;
  the test now uses complete ISO timestamps. Year-range checks pass.
- No implementation or CI failure is currently unresolved locally. Intentional
  mutation failures are regression evidence, not outstanding defects.

## Remaining work

- The owner reports pushing the worker and passing hosted CI. Recorded run URLs
  and independently inspected matrix evidence remain pending (task 4.1).
- Issue-worker orchestration, durable attempt accounting, and failure tracking
  are implemented locally; controlled hosted acceptance remains pending (group 5).
  The independent reviewer is also implemented locally; its hosted check
  attribution and no-bypass merge enforcement remain pending (group 6).
  Automatic merging and publishing still need implementation and live
  verification (groups 6–7).
- No remote activation acceptance run has occurred (task 8.1). Pushing alone
  enables the prepared CI, not the missing worker/review/merge integrations.
- Do not archive bootstrap or claim autonomous maintenance is complete.

## Issue worker implementation intake

- The owner reports creating the GitHub Apps and their private keys and requests
  issue-worker implementation (bootstrap tasks 5.1–5.5).
- Initial rollout: owner-selected `ready` issues, AI-prepared PRs, manual merging,
  and required CI plus independent automated review. Automatic merging remains a
  later activation step, as described in `github-automation-setup-instructions.md`.
- The owner selected OpenAI GPT-6.1 Sol (`openai/gpt-6.1-sol`) and the Actions
  secret name `OPENAI_API_KEY`. No credential values were supplied in conversation
  or committed.
- App installation, stored credentials, hosted execution, and sandbox isolation
  had not been inspected or verified at intake. No remote changes were authorized
  by that intake.

### Issue worker implementation and local verification

- Implemented `.github/workflows/issue-worker.yml`, trusted stdlib Python App/API
  orchestration, durable App-authored issue state, bounded retries and run links,
  per-issue concurrency, event/scheduled reconciliation, PR publication recovery,
  default-branch CI failure deduplication, and manual-merge outcome recording.
- OpenCode 1.19.4 runs each phase in a fresh private directory with only fixed
  sandbox/MCP tools enabled. OpenAI uses `OPENAI_API_KEY`; App keys/tokens are
  excluded from the model process. The MCP process receives a cleared environment.
  Execution containers have no network, credentials, host mounts, or runtime
  sockets. Bounded regular-file patches are published through Git object APIs,
  not executed or applied on the host. The reviewer key is never referenced.
- Verification: `.venv/bin/python scripts/check.py` passes both language suites,
  15 script checks (11 worker checks plus the existing activation/integration
  checks), static checks, and strict validation of all three active changes.
- Verification: image build and `scripts/worker_runtime_check.py --runtime podman`
  pass on this Linux host using rootless Podman. The checks exercise actual
  isolation/hostile symlink rejection, resolved OpenCode permissions, real stdio
  MCP startup, selected-model catalog recognition without a real API key, and
  integrated plus packaged CLI checks in the offline container (Node 22/Python
  3.11). No model request or GitHub write is made by these checks.
- Verification: actionlint 1.7.7 passes both CI and issue-worker workflows.
  Lifecycle tests cover linked PR/evidence creation, questions/duplicates pausing,
  current-head failures, manual-merge completion, unchanged reopen budgets,
  authorized retry, interrupted attempts, lost publication responses, stale issue
  rejection, and rejection of a regression that already passes before the fix.
- Failures resolved: the existing host virtualenv needed its renamed editable
  package reinstalled. Rootless Podman required portable tmpfs options and an
  explicit sandbox-only Git safe.directory; initialization now copies files
  without preserving root ownership. Output is streamed with a bounded memory
  buffer rather than an inherited file-size limit that restricted container
  builds. Offline packaged npm installation required warming registry metadata
  as well as tarballs; the build now warms the real package-install path.
  A failing regression also demonstrated that a disconnected MCP bridge must not
  pass the connection preflight merely because "disconnected" contains
  "connected"; the status now strips terminal color codes and requires the exact
  sandbox/connected words. The real startup check verifies the colored CLI output.
- Task 5.1 is complete with local executable lifecycle evidence. Tasks 5.2–5.5
  remain unchecked pending the controlled hosted acceptance of their implemented
  paths: actual App permissions/token operations, real OpenAI access, GitHub
  event/concurrency/recovery behavior, and linked issue-to-PR evidence. The local
  fake-API checks are not represented as a live GitHub run.
- Activation remains off by default (`ISSUE_WORKER_ENABLED` must explicitly be
  `true`). No worker, reviewer, auto-merger, or publisher is claimed active. No
  secrets were accessed, no remote changes were made, and no push or publishing
  occurred. Independent reviewer implementation and no-bypass current-head merge
  enforcement remain prerequisites for merging worker PRs. Automatic merging
  remains a separate later activation step.
- The current activation report detects an `origin` remote. Its existence does
  not verify hosted CI, installed Apps, stored secrets, or active orchestration;
  none of those remote settings or services was inspected in this session.
- Setup and local reproduction: `docs/issue-worker.md`, primary README commands,
  and `github-automation-setup-instructions.md`. Limits and offline dependency
  behavior are documented. Bootstrap cannot yet be archived.

## Independent reviewer implementation

- Contract: bootstrap task 6.1 and the independently gated merging/credential
  isolation requirements. The owner reports pushing `d00496b` and passing hosted
  CI; no run URL was supplied or independently inspected in this session.
- Implemented `.github/workflows/independent-review.yml`, a fixed trusted review
  policy, and `scripts/independent_review.py`. A separate reviewer App publishes
  `independent-review` on the exact PR head SHA. The shared App-token helper now
  selects explicit implementation/reviewer roles, preserving worker permissions
  and restricting reviewer tokens to contents/PR read plus checks write.
- Review uses a new, tool-free OpenAI Responses request for GPT-6.1 Sol, with
  strict structured output, no prior conversation, and response storage disabled.
  Only task data is sent; App keys/tokens are never put in the prompt. The reviewer
  workflow never references the implementation private key and never executes PR
  code. Privileged checkout is explicitly the trusted default branch; source
  snapshots are immutable API blob data, not executable host files.
- Review input includes supported head source/callers, changed baseline files
  and modes, baseline contracts, linked issue discussions, PR discussions, and
  current-head CI evidence. Unsupported/oversized/truncated input fails closed.
  Changed `.env*`/`.pem`/`.key` paths are blocked before model input; a runnable
  failing check demonstrated the need for that guard before it was added.
- Approvals require matching head/base, complete assessments, no blocking
  findings, and a final unchanged metadata read. Stale output, refusal, malformed
  output, missing provider access, and context failures produce failing checks.
  Earlier same-head success is replaced when input collection fails. Only the
  latest check with matching task/source/policy fingerprint is cached, so
  reverting to rejected PR text cannot leave a newer approval active.
- PR events, explicit dispatch, and scheduled reconciliation are implemented.
  Concurrency is per PR. Cached failures do not automatically spend more tokens;
  an owner-authorized dispatch can retry, with at most three attempts per exact
  context recorded in check-run history. Jobs have 15-minute limits, and the
  model request has a 10-minute timeout and bounded output.
- Verification: `.venv/bin/python scripts/check.py` passes TypeScript and Python
  suites, all 24 script checks (including nine reviewer acceptance checks), static
  checks, and strict validation of all three active OpenSpec changes. Actionlint
  1.7.7 passes CI, worker, and reviewer workflows. App-role checks cover both
  installation-token permission maps and use only synthetic private-key data.
- Reviewer checks cover exact-head approval, new commits during review, blocking
  findings, malformed/refused/tool-call output, oversized/incomplete context,
  prior-approval invalidation, wrong-App spoofing, retry exhaustion, source-as-data
  handling without subprocess execution, and absence of credential values from
  model payloads. A test-fixture omission of the fake App's repository name was
  corrected; there is no unresolved local failure.
- Task 6.1 remains unchecked until a controlled hosted PR verifies reviewer App
  attribution, new-head invalidation, and failure blocking under the actual
  required-check ruleset. Task 6.3's no-bypass/live activation evidence is also
  pending. Bootstrap remains 15/27 complete; do not archive it or call remote
  review active based on these local checks.
- Setup: `docs/independent-review.md` and the updated main setup guide. Configure
  `REVIEWER_APP_PRIVATE_KEY`, `REVIEWER_APP_ID`, and the existing `OPENAI_API_KEY`,
  then explicitly set `INDEPENDENT_REVIEW_ENABLED=true` for a controlled run.
  Manual merging remains the initial rollout. No live App/model request, push,
  remote configuration change, merge, or publication was performed this session.

## Rootprint rename and versioned labels

- Contracts: `openspec/changes/rename-rootprint/` and
  `openspec/changes/version-hash-labels/`, reconciled with the renamed bootstrap
  baseline. The owner explicitly approved renaming the protocol as well as
  packages, imports, CLI commands, maintained references, and source/change paths.
- Decision: use the readable `rootprint-v1` protocol tag. This pre-publication
  rename intentionally changes previous local roots; consumers must recalculate
  them. Labels include `v1` derived from that protocol; label formatting alone
  does not alter its bytes or full digests.
- Permanent requirement: the primary README contains simple usage examples for
  every implementation and copy-and-paste setup/all-tests commands, including
  cross-language integration and installed CLIs. Recorded in `AGENTS.md` and the
  bootstrap maintenance spec; keep it current as ports and test commands evolve.
- Evidence: both language suites and `.venv/bin/python scripts/check.py` pass
  after reinstalling renamed local packages. The independent reference confirms
  all 28 SHA-256 vectors through OpenSSL and the `sum8` vectors by byte sums.
  Both primary README API commands run and produce the committed fixed-clock
  label `20261102_090405-sha256-v1-d331f806a7ada530`.
- Evidence: `.venv/bin/python scripts/package_check.py` passes renamed artifact
  builds, clean-environment installs, both installed `rootprint` console entry
  points, and API examples. `.venv/bin/python scripts/clean_check.py --mutations`
  passes source-only setup/integration/package reproduction and detects all three
  intentional mutations. Its regression assertions now identify tests by stable
  names rather than ordinals. Both primary README stdin CLI examples also run.
- Failure resolved: the first strict validation after moving bootstrap still
  discovered its empty old directories as a change with no deltas. Removing only
  those empty directories restored passing validation for all three active
  changes. No outstanding implementation failure remains locally.
- Environment: these are Linux verification results. The Windows commands are
  documented, but no new Windows/macOS execution is claimed.
- Final inspection: the complete affected implementation and documentation diff
  is reviewed; `git diff --check` passes. A case-insensitive maintained-content
  search and retired-name path glob find no remaining references. Strict
  OpenSpec validation passes all three active changes; its informational archive
  notices correctly reflect the still-unarchived bootstrap baseline.
- Decision: `docs/synchronization.md` describes only a proposed manifest-first
  exchange, batched missing-chunk requests, measured whole-document fallback,
  separately versioned transfer profiles, resource budgets, and final content-root
  verification. No synchronization, tree store, or incremental API is implemented.
  Specify persistent tree storage in a separate change before building sync.
- Archive dependency: bootstrap still supplies the main capabilities and must
  retain its incomplete remote tasks. Dependent deltas must agree on the renamed
  protocol before archive/sync; no change is archived in this session.
- Standing decision: the owner explicitly authorizes local commits for every
  task. Always commit verified agent changes without repeated approval requests;
  preserve human attention for requirements, material ambiguity, and account-owner
  decisions. Recorded permanently in `AGENTS.md`.
- Commit evidence: `fad5bd5` commits the verified rename/label implementation,
  README examples and test commands, synchronization design, and permanent agent
  instructions. The label change's final commit condition is now met; both
  rename and label changes have 6/6 tracked tasks complete. This follow-up records
  completion after the implementation commit actually succeeded. Remote merge
  still requires independent automated review and current-head CI; no push or
  publication is authorized or performed.
