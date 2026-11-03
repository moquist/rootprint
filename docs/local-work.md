# Local work ledger

## Bootstrap

- Contract: `openspec/changes/bootstrap-xmerkle-ecosystem/`.
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

## Remote activation debt

Until pushed, there is no GitHub issue ledger, unattended event-driven worker,
hosted Windows/macOS validation, independent PR review, or enforced merge gate.
The local ledger and Linux checks cover development evidence, not those services.
No scheduled local agent daemon is running.

Before activating: choose repository visibility and license, install a scoped
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
- Built distributions also pass through their installed `xmerkle` console
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
