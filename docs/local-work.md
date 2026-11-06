# Local work ledger

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

- CI workflow is written and linted, but its live matrix is unverified (task 4.1).
- Issue forms and operating contract are prepared. Agent orchestration, durable
  attempt accounting, failure tracking, independent review, automatic merging,
  and publishing still require implementation and live verification (groups 5–7).
- No remote activation acceptance run has occurred (task 8.1). Pushing alone
  enables the prepared CI, not the missing worker/review/merge integrations.
- Do not archive bootstrap or claim autonomous maintenance is complete.

## Issue worker implementation intake

- The owner reports creating the GitHub Apps and their private keys and requests
  issue-worker implementation (bootstrap tasks 5.1–5.5).
- Initial rollout: owner-selected `ready` issues, AI-prepared PRs, manual merging,
  and required CI plus independent automated review. Automatic merging remains a
  later activation step, as described in `github-automation-setup-instructions.md`.
- Implementation is awaiting an account-owner decision on the LLM provider and
  model, plus the name of the Actions secret containing its API credential.
  No credential values should be supplied in conversation or committed.
- App installation, stored credentials, hosted execution, and sandbox isolation
  have not been inspected or verified. No worker is active and no bootstrap task
  is newly complete. No remote changes are authorized by this intake.

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
