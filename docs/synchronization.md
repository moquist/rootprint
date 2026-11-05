# Proposed synchronization design

**Status: design only.** Rootprint has no synchronization API, wire format,
chunker, persistent tree store, or incremental-update API. Current calculations
hash the entire input and discard intermediate nodes. Persistent tree storage
requires its own OpenSpec change before implementing synchronization; this note
does not select a storage schema or promise cached-tree operations.

## Manifest-first exchange

```text
Sender   --> Receiver: target (protocol, algorithm, full root digest)
                       + transfer profile + ordered chunk manifest
Receiver --> Sender:   batched requests for missing chunks
Sender   --> Receiver: requested chunk contents
Receiver: reconstruct, validate JSON, recalculate and verify the target root
```

The manifest identifies each chunk by full digest and length under an explicit
transfer hashing/framing profile. Preserve ordering and repeated references even
when repeated chunk contents are transferred only once. Shortened display labels
are never chunk identifiers or equality checks. Record the content protocol and
transfer profile once where possible rather than repeating long identifiers in
each chunk reference.

This avoids remote walks that require a request for each JSON node or depth.
The receiver compares the manifest with locally available chunks and requests
missing contents in batches. Peers must share a supported content protocol and
provider to verify equality; hex strings calculated under different identities
cannot establish equality. A visible `v1` label alone implements no negotiation.

## Transfer bytes versus content identity

RFC 8785 canonical UTF-8 for the entire document is a candidate transfer object.
It is not the recursive Merkle preimage: hashing that byte stream once does not
produce the `rootprint-v1` root. Chunk boundaries can split encoded tokens;
reassemble bytes before decoding and strict JSON validation.

Content-defined chunking is a candidate for retaining matches after insertions;
fixed offsets can shift all later boundaries. Neither is selected here. Chunk
digests identify bytes under the transfer profile, not JSON-tree node digests.
Verify received chunks and lengths, reconstruct the ordered object, then
recalculate the requested content root. Accept only if the complete
`(protocol, algorithm, digest)` matches the expected target. The expected identity
needs a trusted source; chunk/root consistency alone does not authenticate a peer.

Transfer profiles version wire encoding, chunking parameters, hash framing, and
exchange rules independently of package versions and content protocols. Changing
transfer-side boundaries does not affect `rootprint-v1` identity. If chunk layout
ever becomes part of the committed tree, it is a new root-affecting protocol,
not an option silently introduced under v1.

## Cost-based fallback and bounded exchanges

Choose whole-document transfer when manifest metadata, missing contents, request
framing, and response framing cost as much as or more than the complete encoded
document. Compare costs using the same compression assumptions and include
cache lookup, hashing, and round-trip latency where relevant. Small documents
and low chunk reuse can favor the complete document even when some chunks match.

Manifest bytes grow with chunk count. Batching, paging, and resource limits can
require additional exchanges; this design promises neither universally constant
round trips nor sublinear transferred bytes. Measure complete-document and
chunked-transfer bytes and latency on representative edits before selecting
defaults, including cold-cache and no-change cases.

## Decisions required before implementation

A later implementation proposal must specify:

- The persistent tree/chunk storage contract, cache ownership, retention, and
  how reconstructed bytes relate to stored JSON values.
- Exact transfer bytes, chunk-boundary algorithm and parameters, min/target/max
  chunk sizes, digest algorithm/framing, and empty/repeated-chunk handling.
- Wire serialization, profile identifiers, negotiation, compression, request
  batching/paging, integrity/error handling, and fallback signaling.
- Concrete limits for manifest bytes/entries, chunk and total document sizes,
  nesting, decompression, concurrency, memory, CPU, timeouts, and round trips;
  bounded behavior for malformed or adversarial input.
- Measured byte/latency acceptance criteria versus whole-document transfer,
  resumability/cache behavior, and final-root mismatch rejection.

No network dependency or transport abstraction is needed for the naming/label
changes that document this direction.
