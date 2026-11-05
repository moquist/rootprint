# Design

## Context

See `proposal.md` for motivation. Inspection found only the existing OpenSpec setup and generated local OpenCode tooling: no Git repository, remote, application packages, tests, or published specifications. The configured schema is `spec-driven`. The user approved TypeScript, Python, RFC 8785 semantics, and GitHub/OpenCode automation, and requested timestamped labels.

## Goals / Non-Goals

**Goals:** Establish the exact bytes before implementing either port; expose a small library API plus CLI in each language; make routine maintenance and merges AI-driven and test-gated.

**Non-Goals:** Inclusion proofs, binary balancing, storage engines, incremental updates, network services, arbitrary-precision numeric semantics, and additional language ports. An n-ary JSON-shaped Merkle tree is sufficient for this first protocol.

## Decisions

### 1. A small monorepo with one protocol contract

Use `docs/protocol.md`, `conformance/v1/`, `packages/typescript/`, `packages/python/`, root `AGENTS.md`, and `.github/workflows/`. Keep existing local tooling intact and exclude local node_modules and credentials from version control. Use Node.js 22+ and Python 3.11+; test minimum supported versions and current stable versions where practical. Use each ecosystem's standard package/build tooling and test runner rather than a cross-language orchestration framework.

The independent libraries consume the same committed vectors. Avoid a native shared core or bindings, which would add build and platform complexity before interoperability is established.

### 2. RFC 8785 is a primitive, not the entire Merkle construction

Define `J(x)` as UTF-8 RFC 8785 serialization and `H` as the selected provider. For every JSON node:

```text
scalar(v) = H(J(["rootprint-v1", "value", v]))
array(a)  = H(J(["rootprint-v1", "array", [hex(hash(v)) for v in a]]))
object(o) = H(J(["rootprint-v1", "object", [[k, hex(hash(o[k]))] for k in sortedKeys(o)]]))
```

`hex` is full lowercase hexadecimal; key comparison uses unsigned UTF-16 code units. Scalars are null, booleans, finite binary64 numbers, and valid Unicode strings. The tags distinguish types and containers, JSON serialization provides unambiguous boundaries, and the version tag permits future protocol evolution. Arrays remain ordered; sorting arrays would silently erase JSON meaning. Object member ordering is canonical at every level.

Hashing a whole canonical document once would not produce child commitments. A binary-tree layout would require additional balancing and odd-leaf conventions with no current consumer. Tagged canonical JSON is larger than a binary framing scheme but easier to inspect and implement correctly.

### 3. Strict input validation and tested canonicalization

Use a maintained RFC 8785 implementation in each language rather than reimplementing ECMAScript number formatting. Candidate dependencies are `canonicalize` for TypeScript and `rfc8785` for Python; verify RFC vectors and supported runtime versions before locking dependencies. Python's generic `json.dumps(sort_keys=True)` and TypeScript's default object sorting are not substitutes.

Normalize supported native numeric values to the finite binary64 model, rejecting conversion overflow. JSON numeric tokens use that same model; precision outside it is not promised. Document rounding explicitly, including large integers, and test the boundary cases in both ports. In Python, test booleans before numbers. Reject native unsupported values rather than invoking arbitrary custom serializers. Do not mutate caller objects.

Detect duplicate names before a text parser discards them. Python can use `json.loads` hooks and explicit numeric/constant validation. TypeScript needs a strict token/tree parser retaining member occurrences; use `jsonc-parser` with comments and trailing commas disabled, validate duplicates per object and parser errors, and reject non-JSON extensions. This extra dependency addresses a real gap in `JSON.parse`. Reject lone surrogates, undefined values, sparse arrays, and cyclic inputs. Shared references without cycles remain valid. Handle excessive nesting with an explicit input error rather than producing partial output.

### 4. Minimal algorithm provider API

Use a synchronous provider with identifier, declared digest byte length, and a bytes-to-bytes function. Default to platform SHA-256 (`node:crypto` / `hashlib`); other algorithms are injected by callers, not discovered through a registry or dependency loader. Validate provider identifier, returned type, and output length. Caller responsibility includes deterministic behavior and using the same identifier only for the same algorithm and configuration. Configured variants need distinct identifiers.

This supports any conforming fixed-output algorithm and configured-output XOF. Algorithm names use lowercase ASCII alphanumerics (e.g. `sha256`, `sha3512`, `blake3`) so the display separator is unambiguous. The full identity is `(protocol, algorithm, digest)`; algorithm choice need not be inserted separately into every preimage. Custom-provider tests exercise non-SHA-256 lengths and invocation bytes. The library cannot establish cryptographic strength or prove a callback deterministic.

### 5. Calculation record is separate from content identity

Return a record such as:

```json
{
  "protocol": "rootprint-v1",
  "algorithm": "sha256",
  "digest": "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef",
  "calculatedAt": "2026-11-02T09:04:05Z",
  "label": "20261102_090405-sha256-v1-0123456789abcdef"
}
```

The digest above is illustrative, not a conformance vector. Read the UTC clock once after root calculation, truncate to seconds, and derive both time fields from that instant. Provide a clock injection point and configurable prefix length; default to 16 hex characters or the full digest when shorter. Reject explicit invalid lengths. No timestamp or shortening participates in hashing. Never use labels for equality, proof verification, deduplication, or security decisions. Document that sorting reflects recorded clock time, not causal order.

Both CLIs accept stdin or a file, default SHA-256, and an optional prefix-length argument, emitting exactly this record shape. Keep custom providers in the library API for now; avoid executable plugin resolution from untrusted input.

The `v1` label token is derived from `rootprint-v1`, as specified by
`version-hash-labels`. Archive bootstrap's baseline capability before that
modifying change; this reconciliation does not complete any automation tasks.

The owner subsequently approved `rename-rootprint`, including replacing all
unpublished protocol tags and independently recomputing the changed digests.
Label formatting alone preserves this renamed protocol's bytes. Reconcile all
dependent deltas to this baseline before archive so no old identity is restored.

### 6. Shared expectations, not mutual agreement alone

Vectors include original JSON text, canonical node preimage UTF-8/hex, algorithm, expected full digest, and expected rejection cases. Include RFC numeric boundary vectors, negative zero, escaping, non-BMP versus BMP ordering, composed/decomposed Unicode, reordered object members, ordered arrays, deep nesting, empty containers, and duplicate-name attacks. Independently calculate at least small vectors from literal preimage bytes using platform hashing tools and published RFC examples. Add deterministic fake-provider vectors to expose preimage mistakes without depending on cryptographic collision assumptions.

A six-platform/language CI matrix covers Python and TypeScript on Ubuntu, macOS, and Windows. Use meaningful focused tests plus shared conformance, build/type/static checks, CLI smoke checks, and strict OpenSpec validation. Verify label metadata with a fixed clock so live timestamps cannot make comparisons flaky.

The primary README permanently includes simple usage examples for every
implementation and copy-and-paste setup/test commands covering all
implementations, cross-language integration, and installed distributions. Keep
these current when adding a port or changing test entry points.

### 7. GitHub is the work ledger; OpenSpec is the behavior contract

Root agent instructions require agents to inspect callers, reproduce bugs, consult applicable specs, update planning artifacts for behavior changes, implement, verify, and archive/sync the completed change. Workflow automation can invoke propose/apply/archive as separate phases without requiring a person to author code. Issue states are `triage`, `needs-information`, `ready`, `in-progress`, `blocked`, and `done`; PRs and run links supply the audit trail. Likely duplicates are linked with evidence rather than silently deleted.

Use issue/reopen events plus scheduled reconciliation to avoid dropped events. Permit one active worker per issue, with a 30-minute run limit and at most three implementation attempts per issue revision. Track attempts durably in issue metadata/comments, not ephemeral runner state; new issue information or an explicit retry command can reset a blocked issue. Agent ambiguity becomes an issue question, not a guessed requirement. Failed default-branch CI and broken automation create deduplicated tracking issues; failed fix attempts update the existing issue.

Use a dedicated GitHub App for branch/PR writes and merge operations so generated PRs trigger normal checks; avoid depending on events suppressed for `GITHUB_TOKEN` writes. Agent-generated PRs receive CI and independent automated review from a fresh review context, required on the latest head SHA. Enable automatic squash merge behind a branch ruleset with required named checks, no routine human approval, and no agent bypass. The merge job treats approval output as structured status tied to the reviewed SHA, not prose.

### 8. Isolate privileges from code execution

Use trusted default-branch orchestration for API calls and model access. Execute agent test/build commands and all PR code in disposable credential-free sandboxes, with no host secrets, Docker socket, or write-token mounts. Privileged orchestration retrieves patches/results as untrusted artifacts and publishes them through narrow GitHub API operations. Model credentials remain with the orchestrator; the code-execution sandbox does not receive them. Validate this separation in implementation before enabling autonomy; an environment that cannot isolate execution remains explicitly inactive.

Run PR CI with read-only permissions and no secrets, including fork PRs. Review jobs read diffs as data without executing PR code. Never use a privileged `pull_request_target` job to check out and run PR code. Pin action revisions, keep credentials out of logs and artifacts, and scope provider and GitHub access to the minimum needed. Repository/issue instructions cannot alter trusted orchestration policy. Workflow and agent-policy edits receive explicit independent review under the same merge gates.

This is preferable to giving an unrestricted model-bearing shell repository and publishing credentials. Issue prompt-injection resistance requires the execution boundary, not just a prompt telling the agent to ignore hostile text.

### 9. Releases and activation are explicit states

After initial implementation, use an automated version PR recording package changes and release notes. Once merged through normal gates, tag and build both packages from the verified default-branch SHA and publish through npm/PyPI trusted identity where available. Keep package versions separate from the immutable protocol identifier. Do not auto-publish every merge. Record partial publication failures and retry only missing artifacts; never overwrite an already published version.

Repository creation, Git initialization, credentials, package ownership, license selection, and GitHub App installation are deployment inputs. Do not choose a public/private remote or a license without authorization. Ship a setup checklist and machine-readable activation check; report missing inputs accurately. No manual code editing is required, but account provisioning and decisions about access still need account-owner authority.

## Risks / Trade-offs

- Binary64 can round large integers/decimals → Document the accepted model, test it across ports, and reserve exact-number support for a future protocol.
- Canonicalization dependencies may diverge → Lock versions and require published RFC examples plus independently checked shared vectors.
- Prefix collisions and clock skew → Full digests are authoritative; labels are display metadata, never unique IDs.
- JSON-shaped hashing scales with document size and depth → Fail clearly on resource limits; defer streaming/incremental storage until required.
- Autonomous agents can make incorrect changes → Regression evidence, current-head conformance checks, independent automated review, bounded retries, and revertable commits.
- CI and model execution cost money → Attempt limits, timeouts, concurrency control, and an activation switch; no unbounded self-retry loop.
- Remote settings and credentials are absent → Local implementation can proceed, but activation remains a tracked deployment step.

## Migration Plan

There is no existing data or API to migrate. Implement locally, verify both ports, then activate on an explicitly selected GitHub repository. Configure required checks and App permissions before enabling worker schedules or merge automation. Validate issue-to-PR-to-merge flow with a small tracked change. Publish only after registry ownership and release identity are configured.

Rollback by disabling agent triggers/merge automation, reverting the faulty change through verified CI, and releasing a new package version if needed. Never change published `rootprint-v1` encoding in place or republish a package version with different contents.
