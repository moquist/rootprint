# Tasks

## 1. Repository foundation and protocol

- [x] 1.1 Add the root README, AGENTS.md, ignore rules, and project-specific OpenSpec context describing AI-only implementation and the spec/apply/verify/archive lifecycle; verify instructions reference existing commands and exclude local dependencies and credentials.
- [x] 1.2 Create TypeScript and Python package layouts with standard build/test commands and supported runtime metadata; verify clean installs and empty package builds without altering generated local OpenCode tooling.
- [x] 1.3 Publish `docs/protocol.md` with exact node encoding, UTF-16 ordering, binary64 semantics, provider contract, and full identity versus label distinction; verify worked preimages against all three capability specs.
- [x] 1.4 Commit shared valid/invalid conformance vectors with independently checked scalar/container preimages and digests, RFC numeric/Unicode cases, and deterministic custom-provider cases; verify literal SHA-256 preimages using a separate platform hashing command and record provenance.

## 2. TypeScript library and CLI

- [x] 2.1 Add locked canonicalization and strict JSON parsing dependencies, input validation, UTF-16 sorting, and recursive node hashing; verify shared vectors plus rejection of duplicate keys, non-finite values, lone surrogates, sparse arrays, unsupported native types, and cycles.
- [x] 2.2 Expose SHA-256 and custom-provider APIs with identifier/type/length validation; verify custom-provider preimages, alternate digest lengths, invalid outputs, and absence of caller-input mutation.
- [x] 2.3 Implement full hash records, injected UTC clock, and configurable shortening; verify known-instant labels, timezone independence, same-content/different-time identities, short digests, invalid lengths, and prefix collisions retaining distinct full digests.
- [x] 2.4 Add a file/stdin CLI and API examples; verify packaged CLI smoke checks for valid input, invalid UTF-8/JSON, stdout/stderr discipline, exit codes, and prefix selection, and run documented examples.

## 3. Python library and CLI

- [x] 3.1 Add canonicalization dependency and strict JSON/native-value validation with binary64 normalization and UTF-16 ordering; verify the same shared vectors and rejection cases as TypeScript, including boolean-versus-number handling and large-number rounding parity.
- [x] 3.2 Expose SHA-256 and custom-provider APIs with validation; verify shared custom-provider vectors, alternate lengths, invalid output errors, and no caller-input mutation.
- [x] 3.3 Implement full hash records, UTC clock injection, and configurable shortening; verify the same label and metadata cases used by TypeScript with a fixed clock.
- [x] 3.4 Add packaged file/stdin CLI entry points and API examples; verify clean-environment installation, command output/error behavior, and executable documented examples.

## 4. Required verification pipeline

- [ ] 4.1 Add read-only CI jobs for both language suites on Linux, macOS, and Windows, builds, static/type checks, and strict OpenSpec validation; verify workflow syntax and local equivalents, then verify the matrix when a GitHub remote is available.
- [x] 4.2 Add cross-language integration checks comparing full records under fixed clocks and independently expected vectors, including packaged CLI behavior; verify failures when a canonicalization byte, array order, or digest prefix rule is deliberately perturbed in a disposable copy.
- [x] 4.3 Document required check names, supported runtimes, and local reproduction commands; verify the documented commands complete from a clean checkout.

## 5. Agent-driven issue handling

- [x] 5.1 Add issue forms, durable lifecycle labels, OpenCode worker instructions, and activation/status configuration; verify actionable, duplicate, needs-information, and ambiguous-behavior reports follow the specified transitions with recorded links.
- [ ] 5.2 Implement trusted orchestration with credential-free execution sandboxes and narrow GitHub App API operations; verify adversarial issue/PR content cannot access provider/write secrets through build commands or artifact handling before enabling workers.
- [ ] 5.3 Add issue/reopen triggers and scheduled reconciliation, per-issue concurrency, 30-minute timeouts, and three-attempt durable limits; verify repeated events do not duplicate active workers and exhausted issues remain blocked until eligible retry.
- [ ] 5.4 Connect separate OpenSpec planning, implementation, and completion phases to branch/PR creation; verify a controlled issue produces linked artifacts, regression evidence, a fix PR, and an accurate status comment without human code edits.
- [ ] 5.5 Add deduplicated CI/agent failure tracking and operational documentation; verify repeated failures update one tracking issue and missing credentials yield an explicit inactive status.

## 6. Independent review and merging

- [ ] 6.1 Add fresh-context automated PR review tied to the current head SHA, without executing PR code in the privileged reviewer; verify an approving result becomes stale on a new commit and a failing review blocks merging.
- [ ] 6.2 Add narrowly scoped automatic rebase merging behind required CI and review checks, using App-generated PRs to trigger normal checks; verify squash merging and merge commits are disabled, default-branch history remains linear, failed/missing/stale checks prevent merge, and a fully passing controlled PR merges without human approval.
- [ ] 6.3 Document and expose activation checks for branch rules, no-bypass permissions, App installation, provider credentials, and runner isolation; verify absent configuration reports concrete blockers rather than claiming autonomy is active.

## 7. Release automation

- [ ] 7.1 Add automated version/release-note PR creation and same-revision TypeScript/Python artifact builds, keeping package and protocol versions separate; verify a dry run produces installable artifacts and a linked version PR.
- [ ] 7.2 Add verified-revision publishing with configured registry identity and idempotent recovery from partial publication; verify dry-run refusal on failed checks, missing identity, mismatched revisions, and already-published artifacts.
- [ ] 7.3 Document repository/registry activation inputs, license selection, release operation, and rollback; verify the setup status identifies missing inputs and the documented rollback disables worker/merge triggers without rewriting published history.

## 8. End-to-end acceptance

- [ ] 8.1 Run the complete local integration and strict specification checks and, once activation inputs are supplied, exercise a controlled issue-to-spec-to-fix-to-review-to-merge run; verify its audit trail and all capability acceptance scenarios, recording external blockers explicitly rather than marking unavailable checks complete.

## Workflow follow-up

- Archive this change and synchronize its delta specifications after implementation and verification are complete.
- Verify the resulting main specifications preserve the protocol, record format, and automation requirements.
- Activate the remote workflows and first publication only when account-authorized repository, license, credential, and registry inputs are supplied; incomplete activation tasks remain unchecked until verified.
