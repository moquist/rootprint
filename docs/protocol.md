# rootprint-v1 protocol

This document specifies exact preimage bytes. Until bootstrap is archived, the
OpenSpec delta specifications remain the normative implementation contract.

## Input domain

JSON values: null, boolean, finite IEEE-754 binary64 number, Unicode string,
ordered array, and object with unique string keys. Text must be strict UTF-8
JSON; reject duplicate decoded keys, comments, trailing commas, trailing content,
non-finite/overflowing numbers, and unpaired UTF-16 surrogates. Native input must
not contain cycles, non-string object keys, or language-specific objects.

Numbers have RFC 8785 semantics: `1`, `1.0`, and `1e0` are equivalent; `-0` is
`0`. Numeric input rounds to binary64, including large integer tokens such as
`9007199254740993` (which becomes `9007199254740992`). Exact arbitrary-precision
integers/decimals are unsupported; encode them as strings when exactness matters.
Underflow follows binary64; overflow is rejected. Do not normalize Unicode.

## Merkle construction

Let `J` be RFC 8785 canonical JSON encoded as UTF-8, and `H` the selected hash
provider. Each child digest is represented as its **full lowercase hex** string.

```text
hash(scalar) = H(J(["rootprint-v1", "value", scalar]))
hash(array)  = H(J(["rootprint-v1", "array", [hex(hash(child)), ...]]))
hash(object) = H(J(["rootprint-v1", "object", [[key, hex(hash(value))], ...]]))
```

Arrays retain index order and duplicates. Object pairs sort by key,
lexicographically comparing unsigned UTF-16 code units (not locale, UTF-8 bytes,
or Unicode scalar values). This applies recursively. Empty inputs have distinct
preimages:

| Input | UTF-8 preimage shown as text |
|---|---|
| `null` | `["rootprint-v1","value",null]` |
| `false` | `["rootprint-v1","value",false]` |
| `0` | `["rootprint-v1","value",0]` |
| `"0"` | `["rootprint-v1","value","0"]` |
| `[]` | `["rootprint-v1","array",[]]` |
| `{}` | `["rootprint-v1","object",[]]` |

Tags and JSON framing prevent type/boundary ambiguity before hashing. Actual
digest collisions remain possible for arbitrary providers. This is an n-ary
JSON-shaped Merkle tree, not a balanced binary tree. Every node uses the same
provider; no timestamp, prefix, or locale enters any preimage.

## Hash providers

A provider has a lowercase alphanumeric identifier matching `^[a-z0-9]+$`, a
positive integer digest byte length, and a synchronous bytes-to-bytes function.
Every return must have exactly the declared byte length. The default is
`sha256`, length 32. Use a distinct identifier for each algorithm/configuration,
including a configured XOF output length. Callers are responsible for provider
determinism and cryptographic suitability. Do not load executable providers from
JSON input or CLI names.

## Hash records

Identity is `(protocol, algorithm, digest)`. A calculation returns these fields
and `calculatedAt` (`YYYY-MM-DDTHH:MM:SSZ`) and `label`:

```text
YYYYMMDD_HHMMSS-<algorithm>-<protocol-version>-<digest-prefix>
20261102_090405-sha256-v1-d331f806a7ada530
```

Use root-completion UTC time, read once, truncated to seconds. Years are
0001–9999. Prefix length defaults to min(16, full hex length); an explicitly
requested length must be an integer from 1 through the full hex length.
Never discard the full digest or verify equality using labels. Prefix collisions,
same-second computations, and clock skew mean labels are neither unique IDs nor
authenticated timestamps. Lexicographic sorting orders reported seconds only.

The example is the SHA-256 record for `{"b":2,"a":1}` completed at
`2026-11-02T09:04:05.987Z`, with full digest
`d331f806a7ada5308a00a03f350fd885f492ee54ea4d621af24ef45ba9b88559`.
The `v1` token is derived from the authoritative `protocol: "rootprint-v1"`
field. The shared `sum8` test-provider record for `[1,2]` has label
`20261102_090405-sum8-v1-6f` at that instant. Both examples are committed in
`conformance/v1/records.json`; `sum8` is not cryptographic.

## Independent version domains

| Identity | Identifies |
|---|---|
| Algorithm identifier | Exact hash function/configuration, including configured output length |
| Hashing protocol (`rootprint-v1`) | Canonicalization, framing, tree layout, and all root-affecting parameters |
| Package version | Implementation/API release, independent of content identity |
| Future transfer version/profile | Wire encoding, chunking, manifests, and exchange rules |

Only `rootprint-v1` is implemented; the label token is not protocol negotiation
or a selectable v2 API. Changes to root-affecting rules require a new hashing
protocol, with parameters fixed by it or explicitly identified alongside it.
Changing a label, package release, or transfer-only chunking strategy does not
change `(protocol, algorithm, digest)`. Equal hex digests under different
protocol/provider identities do not establish equal content.

The owner-approved pre-publication rename changed the literal protocol tag and
therefore prior local roots. Recalculate those roots; this was not merely a
display-label change. Published protocol bytes must never change in place.

## Calculation and future storage

Both ports currently calculate every node recursively on each call, returning
only the root record. Intermediate preimages and node digests are temporary;
there is no retained tree, persistence, or incremental-update API. Persistent
tree storage needs a separate specification before synchronization is built.
Storage need not keep repeated protocol tags: a future store can record the
protocol once and reconstruct exact preimages when hashing.

See the [proposed synchronization design](synchronization.md) for transfer-side
chunking, independently versioned profiles, and final Merkle-root verification.

## Compatibility and conformance

Both ports consume `conformance/v1/vectors.json` and `conformance/v1/records.json`.
Expected literal preimages and
digests are committed, not regenerated by a test from the implementation under
test. RFC 8785 numeric examples and UTF-16 ordering exercise canonicalization.
Protocol bytes are immutable after publication; incompatible changes need a new
protocol identifier. Package release versions are independent.
