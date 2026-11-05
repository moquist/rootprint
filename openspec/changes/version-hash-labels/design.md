# Design

## Context

TypeScript `hash` and Python `hash_value` already return a five-field record
whose protocol is `xmerkle-v1`. Their label format includes algorithm and prefix
but omits protocol. `hashJson`/`hash_json` and both CLIs delegate record creation
to those constructors. Both conformance suites assert fixed-clock labels;
`scripts/test_integration.py` checks CLI label shape and cross-language record
equality, including installed packages through `scripts/package_check.py`.

No synchronization API, transport, chunker, or tree exchange exists. The current
Merkle representation follows the JSON structure, potentially producing many
small nodes. There are no published packages or archived main specs yet; the
implemented baseline contract lives in bootstrap's delta specs.

## Goals / Non-Goals

**Goals:** Show hashing-protocol identity in generated labels with the smallest
compatible change to the existing record shape; preserve committed hash bytes;
document synchronization that budgets network round trips and metadata bytes.

**Non-Goals:** Implement a synchronization service, choose a chunking dependency,
introduce a v2 hashing scheme, add application-schema versioning, rename existing
protocol identifiers, or expose an unsupported arbitrary protocol-selection API.

## Decisions

### 1. Include the current protocol's short token in the existing label

Generate:

```text
YYYYMMDD_HHMMSS-<algorithm>-v1-<digest-prefix>
20261102_090405-sha256-v1-0123456789abcdef
```

Derive `v1` from the known `xmerkle-v1` protocol identity in each library's
record-construction path, rather than duplicating label formatting in the CLI.
Keep the existing `protocol` field authoritative; adding a redundant record field
or a separate formatter framework is unnecessary. Algorithm identifiers already
exclude hyphens, so field separation remains straightforward.

Inserting the token after the algorithm follows the user's proposed layout and
retains chronological lexicographic ordering by the leading timestamp. Keep UTC
truncation, year limits, explicit prefix validation, short-provider handling,
and all record field names intact. No fallback legacy label emitter or parser is
needed: neither package is published and neither library currently parses labels.

### 2. Treat version domains separately

| Identity | Meaning |
|---|---|
| Hash algorithm identifier | Exact function/configuration, including output size where applicable |
| Hashing protocol | Canonicalization, node framing, tree layout, and root-affecting parameters |
| Package version | Implementation/API release, independent of hash identity |
| Future synchronization version/profile | Transfer encoding, chunking, manifests, and exchange rules |

The full content identity stays `(protocol, algorithm, digest)`. Changing the
label alone never changes a root. Rebranding the product does not justify
changing `xmerkle-v1` preimage tags. Changes to node encoding, canonicalization,
or root-affecting chunk layout require a different hashing protocol, and any
root-affecting options must be fixed by that protocol or identified alongside it.

Protocol negotiation will be a future synchronization concern. Different
protocol/algorithm identities cannot establish equality just by comparing hex
digests; peers need a common supported identity calculation. Do not imply that
adding a version token implements negotiation.

### 3. Prefer a transfer-side chunk manifest over depth-dependent tree walking

Publish a design note at `docs/synchronization.md` during apply, explicitly
marked as a proposed architecture rather than an implemented API:

```text
Sender   --> Receiver: target content identity + ordered chunk manifest
Receiver --> Sender:   batched missing-chunk requests
Sender   --> Receiver: missing chunk contents
Receiver: reconstruct document, validate JSON, verify target Merkle root
```

This avoids one remote request per JSON tree level or node. The manifest records
ordered chunk identities and lengths; repeated chunks can be referenced more
than once. Chunk identifiers use full digests and an explicitly identified
transfer hashing/framing profile, never shortened display labels.

A candidate byte representation is RFC 8785 canonical UTF-8 for the entire JSON
document. Content-defined boundaries can retain matching chunks after an
insertion where fixed offsets would shift. Those bytes are a transfer object,
not a replacement for the recursive Merkle construction. Reassembly and
recalculation of the target `xmerkle-v1` root remain the final acceptance check.

Transfer-side chunking can evolve independently because it does not enter the
content root. If chunking is later part of the committed tree itself, it becomes
a hashing-protocol change instead. Both choices need explicit versioned rules;
do not silently make arbitrary chunk parameters root-affecting under `v1`.

Choose whole-document transfer when the manifest, missing chunks, and framing
would cost as much as or more than the complete encoded document. The eventual
sync implementation needs bounded manifest/chunk sizes, encoding and integrity
rules, compression accounting, and measured byte/round-trip costs. It must not
claim a universal constant-round-trip or sublinear-byte bound: manifests grow
with chunk count and batching/resource limits may require additional exchanges.

Content-defined chunk parameters, wire serialization, cache persistence, and
concrete budget defaults are prerequisites for that later implementation
proposal, not unresolved blockers for adding the label token now. No chunking
library or speculative transport abstraction is added by this change.

### 4. Preserve the original digest vectors and extend record checks

Add shared fixed-clock record expectations for SHA-256 and the existing `sum8`
test provider. Both language suites consume them and check exact protocol token,
full digest, timestamp, default prefix, and custom-provider behavior. Existing
preimage/digest fixtures remain byte-for-byte unchanged.

Update fixed-clock label assertions and the common CLI helper in
`scripts/test_integration.py`, which also checks installed distributions. Keep
timezone, early-year, collision, array-order, numeric, and prefix-boundary checks.
Run the integrated checker and installed-package checks; no new test framework
or dependency is required.

## Risks / Trade-offs

- Existing callers may split the old three-field label → Document the new shape
  and breaking display change; the five-field record and full identities remain stable.
- Two active changes overlap one requirement → During apply, reconcile the
  bootstrap label requirement and examples with this approved delta and link the
  changes; archive the baseline before this modifying delta. Preserve unrelated
  incomplete automation tasks.
- A visible version could be mistaken for selectable v2 support → State that
  only `xmerkle-v1` is implemented and derive the token from that identity.
- Transfer manifests may exceed small input sizes → Document the whole-document
  fallback and cost measurements required before implementing synchronization.

## Migration Plan

Apply the record/token change to both ports together, update callers/tests/docs,
and reconcile bootstrap's overlapping planning contract. Record the manifest-first
direction in its design note and the local ledger without claiming synchronization
is operational. Validate all active OpenSpec changes and run integrated/package
checks before committing implementation.

No content data migration is needed: existing full roots and preimages remain
valid. If reverting, restore the old label formatting in both ports and tests;
never change protocol bytes merely to roll back a display-format change.
